from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response

from config.permissions import IsAdminOrOperator
from staff.models import Trainer
from .serializers import TrainerSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    """CRUD API for trainers."""

    queryset = Trainer.objects.select_related("user").filter(is_active=True)
    serializer_class = TrainerSerializer
    permission_classes: list = [IsAdminOrOperator]

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """Soft-delete: deactivate trainer instead of deleting."""
        trainer: Trainer = self.get_object()
        trainer.is_active = False
        trainer.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)
