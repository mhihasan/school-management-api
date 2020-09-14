from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Employee
from .models import LegalInformation, Leave
from .models import Designation

from .serializer import EmployeeSerializer, LeaveSerializer, LegalInformationSerializer
from .serializer import DesignationSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["email","date_joined","employee_type","joining_date",
                     "gender","blood_group","gross_salary","designation","sections", "organization"]
    search_fields = ("first_name","last_name","email","gross_salary",)

    ordering_fields = ["first_name", "last_name",
                        "date_joined", "gross_salary"]
    filterset_fields = common_filter


class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    filter_backends = (OrderingFilter,DjangoFilterBackend)
    common_filter = ["employee", "leave_type", "days"]
    ordering_fields = ["days", ]
    filterset_fields = common_filter


class LegalInfoViewSet(viewsets.ModelViewSet):
    queryset = LegalInformation.objects.all()
    serializer_class = LegalInformationSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["employee", "nid"]
    search_fields = ("nid",)
    ordering_fields = ["nid",]
    filterset_fields = common_filter


class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["title", "organization"]
    search_fields = ("title",)
    ordering_fields = ["title",]
    filterset_fields = common_filter

