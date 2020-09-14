from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializer import StudentSerializer, FinancialInfoSerializer, GuardianInfoSerializer
from .models import Student, FinancialInfo, GuardianInfo


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["gender", "roll_no", "organization", "section"]
    search_fields = ("first_name", "last_name", "roll_no", )
    ordering_fields = ["roll_no", "first_name", "last_name"]
    filterset_fields = common_filter


class FinancialInfoViewSet(viewsets.ModelViewSet):
    queryset = FinancialInfo.objects.all()
    serializer_class = FinancialInfoSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["amount", "discount", "student", "fee"]
    ordering_fields = ["amount", "discount", "fee"]
    filterset_fields = common_filter


class GuardianInfoViewSet(viewsets.ModelViewSet):
    queryset = GuardianInfo.objects.all()
    serializer_class = GuardianInfoSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["email", "is_active", "is_guardian", "student"]
    search_fields = ("email","first_name", "last_name",)
    ordering_fields = ["first_name", "email"]
    filterset_fields = [ "email", "is_active", "is_guardian", "student"]


