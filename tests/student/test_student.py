from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
from tests.student.conftest import student_object
from tests.course.conftest import course_object, section_object
import json

from src.student.models import Student
from src.student.serializer import StudentSerializer


class TestStudentViewSet(APITestCase):
    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )
        self.course = course_object(self.organization.id)
        self.section = section_object(self.course.id)
        self.student = student_object(self.section, self.organization)
        self.client.force_authenticate(user=self.admin)


    def test_create_student(self):
        url = "/api/v1/student/"
        data = {"first_name": "adill", "last_name": "rezaaa", "roll_no" : "1312312", "section": self.section.id,
            "present_address" : '[{"name": "kushtia"}]',"permanent_address" : '[{"name": "kushtia"}]',
            "additional_info" : '[{"name": "kushtia"}]',
            "gender":1,
            "organization": self.organization.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(response.data["first_name"], "adill")

    def test_retrieve_student(self):
        url = f"/api/v1/student/{self.student.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        student_serializer_data = StudentSerializer(instance=self.student).data
        response_data = json.loads(response.content)
        self.assertEqual(student_serializer_data, response_data)

    def test_partial_update_student(self):
        url = f"/api/v1/student/{self.student.id}/"
        response = self.client.patch(url, {"last_name": "Reza"})
        response_data = json.loads(response.content)
        changed_data = Student.objects.get(id=self.student.id)
        self.assertEqual(response_data.get("last_name"), changed_data.last_name)

    def test_student_object_delete(self):
        url = f"/api/v1/student/{self.student.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
