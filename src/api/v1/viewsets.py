from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from src.api.v1.permissions import IsAdminStaff


class BaseViewSet(ModelViewSet):
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    permission_classes = (IsAdminStaff,)

    def get_organization_id(self, params):
        if self.request.user.organization_id:
            return self.request.user.organization_id
        elif self.request.user.is_superuser():
            return params.get("organization", None)
        else:
            return 0

    def add_organization_param(self, serializer, params):
        if "organization" in serializer.validated_data:
            del serializer.validated_data["organization"]
        serializer.validated_data.update(
            {"organization_id": self.get_organization_id(params)}
        )

    def perform_create(self, serializer):
        self.add_organization_param(serializer, self.request.POST)
        super().perform_create(serializer)
        return serializer.instance

    def perform_update(self, serializer):
        self.add_organization_param(serializer, self.request.GET)
        super().perform_update(serializer)
        return serializer.instance

    def get_queryset(self):
        organization_id = self.get_organization_id(self.request.GET)
        return super().get_queryset().filter(organization_id=organization_id)
