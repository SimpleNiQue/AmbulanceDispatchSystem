from django.apps import AppConfig

class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.user"

class UserConfig(AppConfig):
    name = 'apps.user'
