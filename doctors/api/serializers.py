from rest_framework import serializers

from doctors.models import SportDoctor


class SportDoctorSerializer(serializers.ModelSerializer):
    """Serializer for SportDoctor model."""

    class Meta:
        model = SportDoctor
        fields: list[str] = [
            "id",
            "first_name",
            "last_name",
            "vat_number",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields: list[str] = ["id", "created_at", "updated_at"]
