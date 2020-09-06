from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        user_attributes = {
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "is_guardian": user.is_guardian,
            "is_admin_staff": user.is_admin_staff,
            "is_superuser": user.is_superuser,
            "organization": user.organization.id,
        }

        for k, v in user_attributes.items():
            token[k] = v

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
