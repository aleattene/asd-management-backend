import logging

from django.core.management.base import BaseCommand

from factories import (
    AthleteFactory,
    CategoryFactory,
    CompanyFactory,
    EnrollmentFactory,
    InvoiceFactory,
    PaymentMethodFactory,
    ReceiptFactory,
    SportCertificateFactory,
    SportDoctorFactory,
    TrainerFactory,
    UserFactory,
)
from users.models import CustomUser, UserRole

logger = logging.getLogger(__name__)

PAYMENT_METHOD_NAMES: list[str] = ["Bonifico Bancario", "Contanti", "POS", "Assegno"]

CATEGORIES: list[dict] = [
    {"code": "U08", "description": "Under 8", "age_range": "6-8"},
    {"code": "U10", "description": "Under 10", "age_range": "9-10"},
    {"code": "U12", "description": "Under 12", "age_range": "11-12"},
    {"code": "U14", "description": "Under 14", "age_range": "13-14"},
    {"code": "U16", "description": "Under 16", "age_range": "15-16"},
    {"code": "U18", "description": "Under 18", "age_range": "17-18"},
    {"code": "SEN", "description": "Senior", "age_range": "18+"},
]


class Command(BaseCommand):
    """Populate the database with realistic development data."""

    help = "Seed the database with development data. Safe to re-run (idempotent)."

    def add_arguments(self, parser) -> None:  # type: ignore[override]
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing data before seeding (except superusers).",
        )

    def handle(self, *args, **options) -> None:
        if options["flush"]:
            self._flush()

        self.stdout.write("Seeding database...")

        payment_methods = self._seed_payment_methods()
        categories = self._seed_categories()
        users = self._seed_users()
        trainers = self._seed_trainers(users["trainers"])
        doctors = self._seed_doctors()
        athletes = self._seed_athletes(users["members"], categories, trainers)
        self._seed_enrollments(athletes)
        self._seed_certificates(athletes, doctors)
        companies = self._seed_companies()
        self._seed_invoices(companies, payment_methods)
        self._seed_receipts(users["members"] + users["trainers"], payment_methods)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _flush(self) -> None:
        """Delete all non-superuser data."""
        from athletes.models import Athlete, Category
        from certificates.models import SportCertificate
        from companies.models import Company
        from doctors.models import SportDoctor
        from enrollments.models import Enrollment
        from invoices.models import Invoice
        from payment_methods.models import PaymentMethod
        from receipts.models import Receipt
        from staff.models import Trainer

        self.stdout.write("Flushing existing data...")
        Receipt.objects.all().delete()
        Invoice.objects.all().delete()
        SportCertificate.objects.all().delete()
        Enrollment.objects.all().delete()
        Athlete.objects.all().delete()
        Trainer.objects.all().delete()
        SportDoctor.objects.all().delete()
        Category.objects.all().delete()
        Company.objects.all().delete()
        PaymentMethod.objects.all().delete()
        CustomUser.objects.filter(is_superuser=False).delete()
        self.stdout.write("Flush complete.")

    def _seed_payment_methods(self) -> list:
        methods = []
        for name in PAYMENT_METHOD_NAMES:
            pm, _ = PaymentMethodFactory._meta.model.objects.get_or_create(name=name)
            methods.append(pm)
        self.stdout.write(f"  Payment methods: {len(methods)}")
        return methods

    def _seed_categories(self) -> list:
        cats = []
        for data in CATEGORIES:
            cat, _ = CategoryFactory._meta.model.objects.get_or_create(
                code=data["code"],
                defaults={"description": data["description"], "age_range": data["age_range"]},
            )
            cats.append(cat)
        self.stdout.write(f"  Categories: {len(cats)}")
        return cats

    def _seed_users(self) -> dict:
        roles: list[dict] = [
            {"role": UserRole.ADMIN, "count": 2, "key": "admins"},
            {"role": UserRole.OPERATOR, "count": 3, "key": "operators"},
            {"role": UserRole.TRAINER, "count": 4, "key": "trainers"},
            {"role": UserRole.MEMBER, "count": 10, "key": "members"},
            {"role": UserRole.EXTERNAL, "count": 3, "key": "externals"},
        ]
        created: dict = {}
        for cfg in roles:
            users = [UserFactory(role=cfg["role"]) for _ in range(cfg["count"])]
            created[cfg["key"]] = users
            self.stdout.write(f"  Users ({cfg['role']}): {len(users)}")

        # Ensure one known superadmin for FE login
        if not CustomUser.objects.filter(username="superadmin").exists():
            CustomUser.objects.create_superuser(
                username="superadmin",
                email="superadmin@asd.local",
                password="Superadmin123!",
            )
            self.stdout.write("  Superadmin created (username: superadmin)")

        # Known admin for FE login
        if not CustomUser.objects.filter(username="admin").exists():
            UserFactory(
                username="admin",
                email="admin@asd.local",
                password=None,
                role=UserRole.ADMIN,
            )
            user = CustomUser.objects.get(username="admin")
            user.set_password("Admin123!")
            user.save()
            self.stdout.write("  Admin created (username: admin)")

        return created

    def _seed_trainers(self, trainer_users: list) -> list:
        trainers = [TrainerFactory(user=u) for u in trainer_users]
        self.stdout.write(f"  Trainers: {len(trainers)}")
        return trainers

    def _seed_doctors(self) -> list:
        doctors = [SportDoctorFactory() for _ in range(3)]
        self.stdout.write(f"  Sport doctors: {len(doctors)}")
        return doctors

    def _seed_athletes(self, guardians: list, categories: list, trainers: list) -> list:
        athletes = []
        for i, guardian in enumerate(guardians):
            category = categories[i % len(categories)]
            trainer = trainers[i % len(trainers)]
            athlete = AthleteFactory(
                guardian=guardian, category=category, trainer=trainer
            )
            athletes.append(athlete)
        # Add a few more athletes without trainer
        for i in range(5):
            athlete = AthleteFactory(
                guardian=guardians[i % len(guardians)],
                category=categories[i % len(categories)],
                trainer=None,
            )
            athletes.append(athlete)
        self.stdout.write(f"  Athletes: {len(athletes)}")
        return athletes

    def _seed_enrollments(self, athletes: list) -> None:
        count = 0
        for athlete in athletes:
            EnrollmentFactory(athlete=athlete, season="2025/2026")
            count += 1
        self.stdout.write(f"  Enrollments: {count}")

    def _seed_certificates(self, athletes: list, doctors: list) -> None:
        count = 0
        for i, athlete in enumerate(athletes[:15]):
            doctor = doctors[i % len(doctors)]
            SportCertificateFactory(athlete=athlete, doctor=doctor)
            count += 1
        self.stdout.write(f"  Certificates: {count}")

    def _seed_companies(self) -> list:
        companies = [CompanyFactory() for _ in range(10)]
        self.stdout.write(f"  Companies: {len(companies)}")
        return companies

    def _seed_invoices(self, companies: list, payment_methods: list) -> None:
        count = 0
        for i in range(20):
            InvoiceFactory(
                company=companies[i % len(companies)],
                payment_method=payment_methods[i % len(payment_methods)],
            )
            count += 1
        self.stdout.write(f"  Invoices: {count}")

    def _seed_receipts(self, users: list, payment_methods: list) -> None:
        count = 0
        for i in range(15):
            ReceiptFactory(
                user=users[i % len(users)],
                payment_method=payment_methods[i % len(payment_methods)],
            )
            count += 1
        self.stdout.write(f"  Receipts: {count}")
