from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from src.user.models import User
from src.user.models import StudentRegistrationForm
from src.user.models import TeacherRecruitment


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)
    organization_text = SerializerMethodField()
    role_text = SerializerMethodField()
    name = SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"

    def get_organization_text(self, ob):
        return ob.cƒompany.name

    def get_role_text(self, ob):
        if ob.role:
            return ob.role.name
        return None

    def get_name(self, ob):
        return ob.get_full_name()


class StudentRegistrationFormSerializer(ModelSerializer):
    class META:
        model = StudentRegistrationForm
        fields = "__all__"
    
class TeacherRecruitmentSerializer(ModelSerializer):
    class META:
        model = TeacherRecruitment
        fields = "__all__"
