# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics

# imported model here
from .models import Course, Subject, Section, Attendance

# imported Serializer 
from .serializers import CourseSerializer, SubjectSerializer, SectionSerializer
from .serializers import AttendanceStudentSerializer, AttendanceTeacherSerializer

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

class AttendanceTeacherViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceTeacherSerializer

class AttendanceStudentViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceStudentSerializer

