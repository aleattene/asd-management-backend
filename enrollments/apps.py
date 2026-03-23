from django.apps import AppConfig


class EnrollmentsConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "enrollments"
    verbose_name: str = "Iscrizioni"
