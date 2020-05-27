from django.contrib.auth.hashers import make_password

# Create your views here.
from src.api.v1.viewsets import BaseViewSet
from src.user.models import User
from src.user.serializers import UserSerializer


class UserViewSet(BaseViewSet):
    queryset = User.objects.select_related("organization")
    serializer_class = UserSerializer
    search_fields = ("first_name", "last_name")

    def perform_create(self, serializer):
        password = serializer.validated_data.pop("password", None)
        organization = serializer.validated_data.pop("organization", None)

        if password:
            serializer.validated_data.update({"password": make_password(password)})

        if organization and (
            self.request.user.is_admin_staff or self.request.user.is_superuser
        ):
            serializer.validated_data.update({"organization": organization})
            serializer.save()
        else:
            return super().perform_create(serializer)

    def perform_update(self, serializer):
        serializer.validated_data.pop("password", None)
        return super().perform_update(serializer)
