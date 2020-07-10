from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
from tests.student.conftest import student_object, guardian_info_object
from tests.course.conftest import course_object, section_object
import json

# imported serializer and model
from src.student.models import GuardianInfo

from src.student.serializer import GuardianInfoSerializer


class TestGuardianInfoViewSet(APITestCase):
    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )
        self.course = course_object(self.organization.id)
        self.section = section_object(self.course.id)
        self.student = student_object(self.section, self.organization)
        self.guardian_info = guardian_info_object(self.student, "adilr3344@gmail.com")
        self.client.force_authenticate(user=self.admin)

    def test_create_guardian_info(self):
        url = "/api/v1/student/guadianinfo/"
        data = {
                "student":self.student.id,
                "first_name": "Nakib",
                "email": "nakibhossain@gmail.com",
                "relationship": "friend",
                "is_guardian": True,
                "phone":"01782334457"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GuardianInfo.objects.count(), 2)
        self.assertEqual(response.data["first_name"], "Nakib")

    def test_retrieve_guardian_info(self):
        url = f"/api/v1/student/guadianinfo/{self.guardian_info.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        guardian_info_serializer_data = GuardianInfoSerializer(instance=self.guardian_info).data
        response_data = json.loads(response.content)
        self.assertEqual(guardian_info_serializer_data, response_data)

    def test_partial_update_guardian_info(self):
        url = f"/api/v1/student/guadianinfo/{self.guardian_info.id}/"
        response = self.client.patch(url, {"relationship": "self_adil"})
        response_data = json.loads(response.content)
        changed_data = GuardianInfo.objects.get(id=self.guardian_info.id)
        self.assertEqual(response_data.get("relationship"), changed_data.relationship)

    def test_guardian_info_object_delete(self):
        url = f"/api/v1/student/guadianinfo/{self.guardian_info.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
