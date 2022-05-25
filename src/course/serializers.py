from rest_framework import serializers

from .models import Course, Section, Subject, Attendance


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id","name","organization"]


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id","name","course"]


class SubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField("get_teacher_name")
    class Meta:
        model = Subject
        fields = ["id","name","course","teacher", "teacher_name"]

    def get_teacher_name(self, obj):
        return obj.teacher.first_name + " "+ obj.teacher.last_name



class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
