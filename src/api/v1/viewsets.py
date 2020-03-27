from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import ModelPermissions, IsStaff


class BaseViewSet(ModelViewSet):
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    permission_classes = (IsStaff, ModelPermissions)

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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
