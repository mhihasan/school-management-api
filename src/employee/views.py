# from django.shortcuts import render
from rest_framework import viewsets
#from rest_framework import generics

# import model here 
from .models import Employee
from .models import LegalInformation, Leave

# imported Serializer
from .serializer import EmployeeSerializer, LeaveSerializer, LegalInformationSerializer

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
