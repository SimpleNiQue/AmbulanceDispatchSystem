from django.urls import path
from apps.user.v1.views.auth import (
    UserSignUpView,
    EmailVerifyView,
    LoginView,
    RefreshTokenView,
    LogoutView,
    ResendEmailView,
    PasswordTokenCheckAPI,
    SetNewPasswordAPIView,
    ValidateOTPAndResetPassword,
    RequestPasswordResetOTPView,
    GetUsersView
)

urlpatterns = [
    path("", GetUsersView.as_view(), name="get-users"),
    path("signup/", UserSignUpView.as_view(), name="user-signup"),
    path("email/verify/", EmailVerifyView.as_view(), name="email-verify"),
    path("email/resend/", ResendEmailView.as_view(), name="resend-email"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordTokenCheckAPI.as_view(),
        name="password-token-check",
    ),
    path("password-reset/confirm/", SetNewPasswordAPIView.as_view(), name="password-reset-confirm"),
    path("reset-password/validate", ValidateOTPAndResetPassword.as_view(), name="validate-otp-password-reset"),
    path("reset-password", RequestPasswordResetOTPView.as_view(), name="request-password-reset-otp"),
]
