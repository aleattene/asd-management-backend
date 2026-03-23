import re

from django.core.exceptions import ValidationError
from django.db import models


def validate_season(value: str) -> None:
    """Validate season format YYYY/YYYY with consecutive years (e.g. 2025/2026)."""
    if not re.match(r"^\d{4}/\d{4}$", value):
        raise ValidationError("Season must be in format YYYY/YYYY (e.g. 2025/2026).")
    year1, year2 = int(value[:4]), int(value[5:])
    if year2 != year1 + 1:
        raise ValidationError("Season years must be consecutive (e.g. 2025/2026).")


class Enrollment(models.Model):
    """Model representing an athlete's enrollment for a sports season."""

    athlete = models.ForeignKey(
        "athletes.Athlete",
        on_delete=models.PROTECT,
        related_name="enrollments",
        verbose_name="Atleta",
    )
    season = models.CharField(
        max_length=9,
        validators=[validate_season],
        verbose_name="Stagione",
    )
    enrollment_date = models.DateField(verbose_name="Data Iscrizione")
    guardian_signed = models.BooleanField(
        default=False,
        verbose_name="Firma Tutore",
    )
    is_active = models.BooleanField(default=True, verbose_name="Attivo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Iscrizione"
        verbose_name_plural = "Iscrizioni"
        ordering = ["-season", "athlete"]
        constraints = [
            models.UniqueConstraint(
                fields=["athlete", "season"],
                name="unique_enrollment_per_season",
            )
        ]

    def __str__(self) -> str:
        return f"{self.athlete} — {self.season}"

    def __repr__(self) -> str:
        return f"Enrollment(athlete_id={self.athlete_id}, season={self.season!r})"
