from django.db import IntegrityError
from django.test import TestCase

from doctors.models import SportDoctor


class SportDoctorModelTests(TestCase):
    """Tests for SportDoctor model."""

    def setUp(self) -> None:
        self.doctor: SportDoctor = SportDoctor.objects.create(
            first_name="Giuseppe",
            last_name="Verdi",
            vat_number="12345678901",
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.doctor), "Verdi Giuseppe (P.IVA: 12345678901)")

    def test_repr(self) -> None:
        self.assertIn("SportDoctor(", repr(self.doctor))

    def test_vat_number_unique(self) -> None:
        with self.assertRaises(IntegrityError):
            SportDoctor.objects.create(
                first_name="Clone",
                last_name="Clone",
                vat_number="12345678901",
            )

    def test_is_active_default_true(self) -> None:
        self.assertTrue(self.doctor.is_active)
