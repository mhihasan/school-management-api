from rest_framework import serializers


# imported model here
from .models import Course, Section, Subject, Attendance

# serializer here
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["name","organization"]

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["name","course"]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name","course","teacher"]

class AttendanceTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["employee","date","is_present"]

class AttendanceStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["student", "date", "is_present"]
