from rest_framework.serializers import ModelSerializer

from src.organization.models import Organization


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
