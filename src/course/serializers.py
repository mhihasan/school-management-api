from rest_framework import serializers


# imported model here
from .models import Course, Section, Subject, Attendance

# serializer here
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id","name","organization"]

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id","name","course"]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id","name","course","teacher"]

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
