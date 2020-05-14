from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .permissions import ModelPermissions, IsAdminStaff


class BaseViewSet(ModelViewSet):
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    permission_classes = (IsAdminStaff, ModelPermissions)

    def get_organization_id(self):
        return (
            self.request.user.organization_id
            if self.request.user.organization_id
            else 0
        )

    def add_organization_param(self, serializer):
        if "organization" in serializer.validated_data:
            del serializer.validated_data["organization"]
        serializer.validated_data.update(
            {"organization_id": self.get_organization_id()}
        )

    def perform_create(self, serializer):
        self.add_organization_param(serializer)
        super().perform_create(serializer)
        return serializer.instance

    def perform_update(self, serializer):
        self.add_organization_param(serializer)
        super().perform_update(serializer)
        return serializer.instance

    def get_queryset(self):
        organization_id = self.get_organization_id()
        return super().get_queryset().filter(organization_id=organization_id)
