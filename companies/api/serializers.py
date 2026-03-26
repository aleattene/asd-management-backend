from rest_framework import serializers

from companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company model."""

    class Meta:
        model = Company
        fields: list[str] = [
            "id",
            "business_name",
            "vat_number",
            "fiscal_code",
            "vat_equals_fc",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "created_at", "updated_at"]
