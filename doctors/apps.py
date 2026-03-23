from django.apps import AppConfig


class DoctorsConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "doctors"
    verbose_name: str = "Medici Sportivi"
