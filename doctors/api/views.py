from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from config.permissions import IsAdminOrOperator
from doctors.models import SportDoctor
from .serializers import SportDoctorSerializer


class SportDoctorViewSet(viewsets.ModelViewSet):
    """CRUD API for sport doctors."""

    queryset = SportDoctor.objects.filter(is_active=True)
    serializer_class = SportDoctorSerializer
    permission_classes: list = [IsAdminOrOperator]

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Soft-delete: deactivate doctor instead of deleting."""
        doctor: SportDoctor = self.get_object()
        doctor.is_active = False
        doctor.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)
