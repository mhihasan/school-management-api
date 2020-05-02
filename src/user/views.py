from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from src.api.v1.permissions import ModelPermissions
from src.api.v1.viewsets import BaseViewSet
from src.user.serializers import UserSerializer
from src.user.serializers import students_serializer
from src.user.serializers import teachers_serializer

# Here imported model
from src.user.models import User
from src.user.models import students
from src.user.models import Teachers


class UserViewSet(BaseViewSet):
    queryset = User.objects.select_related("role", "company")
    serializer_class = UserSerializer
    permission_classes = (ModelPermissions,)
    search_fields = ("first_name", "last_name")

    def perform_create(self, serializer):
        password = serializer.validated_data.pop("password", None)
        company = serializer.validated_data.pop("company", None)

        if password:
            serializer.validated_data.update({"password": make_password(password)})

        if company and (self.request.user.is_admin() or self.request.user.is_superuser):
            serializer.validated_data.update({"company": company})
            serializer.save()
        else:
            return super().perform_create(serializer)

    def perform_update(self, serializer):
        serializer.validated_data.pop("password", None)
        return super().perform_update(serializer)

class students_viewset(viewsets.ModelViewSet):
    queryset = students.objects.all()
    serializer_class = students_serializer

class teachers_viewset(viewsets.ModelViewSet):
    queryset = Teachers.objects.all()
    serializer_class = teachers_serializer