from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from src.user.models import User


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)
    organization_text = SerializerMethodField()
    name = SerializerMethodField()

    class Meta:
        model = User
        exclude = ["groups", "user_permissions"]

    def get_organization_text(self, ob):
        return ob.organization.name if ob.organization else None

    def get_name(self, ob):
        return ob.get_full_name()
