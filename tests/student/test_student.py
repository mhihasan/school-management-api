from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
from tests.student.conftest import student_object, course_object, section_object
import json

# imported serializer and model
from src.student.models import Student


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
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(response.data["first_name"], "adill")

    