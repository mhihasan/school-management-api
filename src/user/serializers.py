from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from src.user.models import User
from src.user.models import students
from src.user.models import Teachers


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)
    organization_text = SerializerMethodField()
    role_text = SerializerMethodField()
    name = SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"

    def get_organization_text(self, ob):
        return ob.company.name

    def get_role_text(self, ob):
        if ob.role:
            return ob.role.name
        return None

    def get_name(self, ob):
        return ob.get_full_name()


class students_serializer(ModelSerializer):
    class META:
        model = students
        fields = "__all__"
    
class teachers_serializer(ModelSerializer):
    class META:
        model = Teachers
        fields = "__all__"
