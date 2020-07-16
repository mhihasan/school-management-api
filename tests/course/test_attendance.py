from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
import json
from tests.course.conftest import teacher_object, section_object, course_object, attendance_object
from tests.student.conftest import student_object
from src.course.models import Attendance
from src.course.serializers import AttendanceSerializer


class TestAttendanceViewSet(APITestCase):
    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )
        self.course = course_object(self.organization.id)
        self.section = section_object(self.course.id)
        self.teacher = teacher_object("adilreza09787778@gmail.com")
        self.student = student_object(self.section, self.organization)
        self.attendance = attendance_object(self.teacher, self.student)

    def test_create_attendance(self):
        url = "/api/v1/attendance/"
        data = {"employee": self.teacher.id,"student": self.student.id, "is_present":False}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 2)

    def test_retrieve_attendance(self):
        url = f"/api/v1/attendance/{self.attendance.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        attendance_serializer_data = AttendanceSerializer(instance=self.attendance).data
        response_data = json.loads(response.content)
        self.assertEqual(attendance_serializer_data, response_data)

    def test_partial_update_attendance(self):
        url = f"/api/v1/attendance/{self.attendance.id}/"
        response = self.client.patch(url, {"is_present": True})
        response_data = json.loads(response.content)
        changed_att = Attendance.objects.get(id=self.attendance.id)
        self.assertEqual(response_data.get("is_present"), changed_att.is_present)

    def test_attendance_object_delete(self):
        url = f"/api/v1/attendance/{self.attendance.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)

