# from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
#from rest_framework import generics

# import model here 
from .models import Employee
from .models import LegalInformation, Leave
from .models import Designation

# imported Serializer
from .serializer import EmployeeSerializer, LeaveSerializer, LegalInformationSerializer
from .serializer import DesignationSerializer

# Create your views here.


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["first_name", "last_name","email",
                     "date_joined","employee_type","joining_date",
                     "gender","blood_group","gross_salary","designation","sections"]
    search_fields = common_filter
    ordering_fields = common_filter
    filterset_fields = common_filter


class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["employee", "leave_type","days"]
    search_fields = common_filter
    ordering_fields = common_filter
    filterset_fields = common_filter


class LegalInfoViewSet(viewsets.ModelViewSet):
    queryset = LegalInformation.objects.all()
    serializer_class = LegalInformationSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["employee","nid"]
    search_fields = common_filter
    ordering_fields = common_filter
    filterset_fields = common_filter


class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["title", "organization"]
    search_fields = common_filter
    ordering_fields = common_filter
    filterset_fields = common_filter

