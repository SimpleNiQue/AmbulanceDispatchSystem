from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.core.cache import cache
from django.core.signing import BadSignature, Signer
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode
from jwt.exceptions import ExpiredSignatureError
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

from apps.user.v1.serializers.auth import (
    EmailVerifySerializer,
    LoginSerializer,
    PasswordResetTokenGenerator,
    RefreshTokenSerializer,
    ResendEmailSerializer,
    ResetPasswordSerializer,
    SetNewPasswordSerializer,
    UserSignUpSerializer,
    UserSerializer
)
from utils.responses import CustomRedirect, api_response
from utils.exceptions import CustomExceptions, handle_exception
from utils.mailing import email_service

User = get_user_model()

class UserSignUpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignUpSerializer

    @transaction.atomic
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        try:
            return api_response(
                status=status.HTTP_201_CREATED,
                data=None,
                message="Registration successful!",
            )
        except Exception as e:
            handle_exception(
                "Failed to send verification email",
                CustomExceptions.EMAIL_ERROR,
                logger_name=__name__,
                exception=e,
            )


class VerifiedUserBackend(BaseBackend):
    def authenticate(
        self, request: Request, username: str = None, password: str = None
    ) -> Response:
        try:
            user = User.objects.get(username=username)
            return user if user.check_password(password) and user.is_verified else None

        except User.DoesNotExist:
            handle_exception(
                None,
                CustomExceptions.NOT_FOUND,
                message=f"Authentication failed: User '{username}' does not exist.",
                logger_name=__name__,
            )

        return None


class ResendEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data["email"])
            email_service.send_signup_verification_email(request, user)
            return api_response(message="Verification email resent successfully.")

        except User.DoesNotExist:
            handle_exception(
                "User not found.",
                CustomExceptions.NOT_FOUND,
                logger_name=__name__,
            )


class EmailVerifyView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email = Signer().unsign(serializer.validated_data["token"])
            user = User.objects.get(email=email)
            user.is_verified = True
            user.save()
            return api_response(message="Email successfully verified.")
        except (BadSignature, User.DoesNotExist) as e:
            handle_exception(
                "Invalid or expired token.",
                logger_name=__name__,
                exception=e,
            )



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return api_response(
            message="Login successful.",
            data={
                "role": user.role,
                "accessToken": str(refresh.access_token),
                "refreshToken": str(refresh),
            },
        )


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_refresh_token = serializer.validated_data["refreshToken"]

        try:
            refresh = RefreshToken(old_refresh_token)
            response = RefreshTokenSerializer(
                {
                    "accessToken": str(refresh.access_token),
                    "refreshToken": str(refresh),
                }
            )

            return api_response(
                message="Refresh token obtained",
                data=response.data,
            )

        except Exception as e:
            return handle_exception(
                data={"error": "Invalid or expired refresh token"},
                exception_enum=CustomExceptions.BAD_REQUEST,
                logger_name=__name__,
                exception=e,
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            handle_exception(
                "Refresh token is required.",
            )

        try:
            RefreshToken(refresh_token).blacklist()
            return api_response(message="Logout successful.")

        except (ExpiredSignatureError, Exception) as e:
            handle_exception(
                "Invalid or expired refresh token.",
                logger_name=__name__,
                exception=e,
            )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):
        redirect_url = request.GET.get("redirect_url", "http://localhost:3000")
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return CustomRedirect(
                    f"{redirect_url}?token_valid=False&message=Invalid or expired token"
                )
            return CustomRedirect(
                f"{redirect_url}?token_valid=True&message=Credentials Valid&uidb64={uidb64}&token={token}"
            )

        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            handle_exception("Invalid or expired token.")


class SetNewPasswordAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return api_response(message="Password reset successful.")


class ValidateOTPAndResetPassword(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    @transaction.atomic
    def post(self, request):
        email, auth_code, new_password = map(
            str.strip,
            [
                request.data.get("email", ""),
                request.data.get("auth_code", ""),
                request.data.get("new_password", ""),
            ],
        )

        if not all([email, auth_code, new_password]):
            handle_exception("All fields are required.")

        try:
            auth_code = int(auth_code)
            stored_auth_code = int(cache.get(f"password_reset_code_{email}", 0))
            if stored_auth_code != auth_code:
                handle_exception("Invalid OTP.")

            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            cache.delete(f"password_reset_code_{email}")
            return api_response(message="Password reset successful.")
        except (ValueError, User.DoesNotExist):
            handle_exception("Invalid request data.")
            
class GetUsersView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()  # uses self.queryset correctly
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            return qs.filter(is_active=is_active.lower() == "true")
        return qs
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return api_response(
            status=status.HTTP_200_OK,
            message="Users retrieved successfully.",
            data=serializer.data,
        )
