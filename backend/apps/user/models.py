from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.utils import UserTypesEnum, DB_NAMES, GenderEnum
from utils.mixins import Audit


class User(AbstractUser, Audit):
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    role = models.CharField(
        max_length=20, choices=UserTypesEnum.options(), default=UserTypesEnum.PATIENT
    )
    terms_of_service_agreement_checked = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        db_table = DB_NAMES.User
        ordering = ["-date_created"]


class Profile(Audit):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    gender = models.CharField(
        max_length=7, choices=GenderEnum.options(), blank=True, null=True
    )
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )

    def __str__(self):
        return f"Profile for {self.user.first_name}"

    class Meta:
        db_table = DB_NAMES.Profile
