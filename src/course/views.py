# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics

# imported model here
from .models import Course, Subject, Section, Attendance

# imported Serializer 
from .serializers import CourseSerializer, SubjectSerializer, SectionSerializer
from .serializers import AttendanceSerializer

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    # queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    def get_queryset(self):
        queryset = self.queryset
        person = self.request.query_params.get('student','')
        person2 = self.request.query_params.get('employee','')
        if person:
            query_set = queryset.filter(student=person)
            return query_set
        elif person2:
            query_set = queryset.filter(employee=person2)
            return query_set
        else:
            return queryset

