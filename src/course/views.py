# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# imported model here
from .models import Course, Subject, Section, Attendance

# imported Serializer 
from .serializers import CourseSerializer, SubjectSerializer, SectionSerializer
from .serializers import AttendanceSerializer

# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["name","organization"]
    search_fields = common_filter
    ordering_fields = common_filter
    filterset_fields = common_filter


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["name", "course", "teacher"]
    search_fields = common_filter
    ordering_fields = common_filter
    filterset_fields = common_filter


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["name", "course"]
    search_fields = common_filter
    ordering_fields = common_filter
    filterset_fields = common_filter


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    common_filter = ["date","is_present", "student", "employee"]
    search_fields = ["student", "employee"]
    ordering_fields = ["date", "student", "employee"]
    filterset_fields = common_filter


