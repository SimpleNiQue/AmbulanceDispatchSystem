from __future__ import annotations

import logging
import mimetypes

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode
from utils.tasks import send_email_task

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self, default_sender=None):
        self.user_template = "user"
        self.default_sender = default_sender or settings.DEFAULT_FROM_EMAIL

    def send_email(
        self, subject, recipient_email, template_name, context, attachements=None
    ):
        context["from_email"] = self.default_sender

        send_email_task(
            subject, recipient_email, template_name, context, attachements
        )

    def send_signup_verification_email(self, request, user):
        first_name = user.first_name
        verification_url = self.create_verification_url(request, user.email)

        context = {
            "first_name": first_name,
            "verification_url": verification_url,
        }
        self.send_email(
            subject="ADS Account Verification",
            recipient_email=user.email,
            template_name=f"{self.user_template}/verification.html",
            context=context,
        )

    def create_verification_url(self, request, email):
        from django.core.signing import Signer

        signer = Signer()
        token = signer.sign(email)

        return f"{request.scheme}://{get_current_site(request).domain}/user/verify/?token={token}"

    def send_password_reset_email(self, request, user_obj):
        domain = get_current_site(request).domain
        scheme = request.scheme

        uidb64 = urlsafe_base64_encode(str(user_obj.id).encode())
        token = PasswordResetTokenGenerator().make_token(user_obj)
        reset_code = get_random_string(length=6, allowed_chars="0123456789")
        cache.set(f"password_reset_code_{user_obj.email}", reset_code, timeout=900)

        reset_url = f"{scheme}://{domain}{reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})}"

        context = {"reset_url": reset_url, "reset_code": reset_code}
        self.send_email(
            subject="Reset Your Password",
            recipient_email=user_obj.email,
            template_name=f"{self.user_template}/password_reset.html",
            context=context,
        )

email_service: EmailService = EmailService()