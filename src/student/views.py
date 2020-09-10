from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from src.user.models import User
from django.http import HttpResponse

# imported serializer
from .serializer import StudentSerializer, FinancialInfoSerializer, GuardianInfoSerializer

# imported Model
from .models import Student, FinancialInfo, GuardianInfo

# Create your views here.


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["gender", "roll_no","organization", "section"]
    search_fields = ("roll_no","organization")
    ordering_fields = ["roll_no", "section"]
    filterset_fields = common_filter


class FinancialInfoViewSet(viewsets.ModelViewSet):
    queryset = FinancialInfo.objects.all()
    serializer_class = FinancialInfoSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["amount", "discount", "student", "fee"]
    ordering_fields = common_filter
    filterset_fields = common_filter


class GuardianInfoViewSet(viewsets.ModelViewSet):
    queryset = GuardianInfo.objects.all()
    serializer_class = GuardianInfoSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["first_name", "last_name", "email", "is_active", "is_guardian", "relationship", "student"]
    search_fields = ("email",)
    ordering_fields = ["first_name", "email", "relationship","student"]
    filterset_fields = [ "email", "is_active", "is_guardian", "relationship", "student"]


