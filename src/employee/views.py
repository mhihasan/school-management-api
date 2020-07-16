# from django.shortcuts import render
from rest_framework import viewsets
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

class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

class LegalInfoViewSet(viewsets.ModelViewSet):
    queryset = LegalInformation.objects.all()
    serializer_class = LegalInformationSerializer
    def get_queryset(self):
        queryset = self.queryset
        employee = self.request.query_params.get('employee','')
        if employee:
            query_set = queryset.filter(employee=employee)
            return query_set
        else:
            return queryset

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer