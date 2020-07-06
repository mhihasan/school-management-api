from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
from tests.course.conftest import course_object, section_object
import json

# imported serializer and model
from src.course.models import Section
from src.course.serializers import SectionSerializer
from src.course.models import Course


class TestSectionViewSet(APITestCase):
    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )
        self.course = course_object(self.organization.id)
        self.section = section_object(self.course.id)

    def test_create_section(self):
        url = "/api/v1/section/"
        data = {"name": "kodom2", "course": self.course.id}

        response = self.client.post(url, data, format="json")
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)

    def test_retrieve_section(self):
        url = f"/api/v1/section/{self.section.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        section_serializer_data = SectionSerializer(instance=self.section).data
        response_data = json.loads(response.content)
        self.assertEqual(section_serializer_data, response_data)

    def test_partial_update_section(self):
        url = f"/api/v1/section/{self.section.id}/"
        response = self.client.patch(url, {"name": "something"})
        response_data = json.loads(response.content)
        changed_section = Section.objects.get(id=self.section.id)
        self.assertEqual(response_data.get("name"), changed_section.name)

    def test_section_object_delete(self):
        url = f"/api/v1/section/{self.section.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
