from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from apps.user.models import Profile
from utils.exceptions import (
    ValidationError,
    handle_exception,
)

User = get_user_model()


class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                {"email": "User with the provided email does not exist."}
            )
        if user.is_verified:
            raise ValidationError({"email": "Account is already verified."})

        return {"user": user}


class UserSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(
        source="first_name",
    )
    lastName = serializers.CharField(
        source="last_name",
    )
    termsOfServiceAgreementChecked = serializers.BooleanField(
        source="terms_of_service_agreement_checked",
    )
    isVerified = serializers.BooleanField(source="is_verified", read_only=True)
    isActive = serializers.BooleanField(source="is_active", read_only=True)
    dateCreated = serializers.DateTimeField(source="date_created")
    lastUpdated = serializers.DateTimeField(source="last_updated")
    uniqueId = serializers.CharField(source="unique_id", read_only=True)

    class Meta:
        model = User
        fields = [
            "uniqueId",
            "email",
            "firstName",
            "lastName",
            "role",
            "isVerified",
            "isActive",
            "dateCreated",
            "lastUpdated",
            "termsOfServiceAgreementChecked",
        ]


class UserSignUpSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(
        error_messages={
            "required": "Email is required",
            "invalid": "Invalid email format",
            "unique": "This email is already registered!",
        }
    )
    firstName = serializers.CharField(
        error_messages={
            "required": "First name is required",
            "blank": "First name is required",
        },
        source="first_name",
    )
    lastName = serializers.CharField(
        error_messages={
            "required": "Last name is required",
            "blank": "Last name is required",
        },
        source="last_name",
    )
    termsOfServiceAgreementChecked = serializers.BooleanField(
        error_messages={
            "required": "agreement to terms of service is required before signing up",
            "blank": "agreement to terms of service is required before signing up",
        },
        source="terms_of_service_agreement_checked",
    )

    class Meta:
        model = User
        fields = (
            "firstName",
            "lastName",
            "email",
            "password",
            "role",
            "termsOfServiceAgreementChecked",
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            handle_exception("A user with this email already exists.")

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data["email"]
        username = email.split("@")[0]

        while User.objects.filter(username=username).exists():
            username += str(User.objects.count())

        validated_data["username"] = username
        user = User.objects.create_user(password=password, **validated_data)

        with transaction.atomic():
            Profile.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email, password = data.get("email"), data.get("password")
        user = User.objects.filter(email=email).first()

        if not user or not check_password(password, user.password):
            handle_exception(
                "Invalid email/password combination.",
            )
        if not user.is_active:
            handle_exception(
                "User account is disabled.",
            )

        return user


class RefreshTokenSerializer(serializers.Serializer):
    refreshToken = serializers.CharField(
        error_messages={
            "required": "Refresh token is required",
            "blank": "Refresh token cannot be blank",
        }
    )
    accessToken = serializers.CharField(read_only=True)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uidb64"]))
            user = User.objects.get(id=uid)
            if not PasswordResetTokenGenerator().check_token(user, attrs["token"]):
                raise AuthenticationFailed("Invalid reset link.")

            user.set_password(attrs["password"])
            user.save()
            return {"user": user}
        except (User.DoesNotExist, ValueError, TypeError):
            raise AuthenticationFailed("Invalid reset link.")


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    auth_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8)


class RequestPasswordResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                {"email": "User with the provided email does not exist."}
            )

        return {"user": user}


class EmailVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        try:
            email = str(value).split(":")[0]
            user = User.objects.get(email=email)
            if user.is_verified:
                handle_exception(
                    data={"token": "User already verified"},
                )

            return value
        except User.DoesNotExist:
            handle_exception("User not found")