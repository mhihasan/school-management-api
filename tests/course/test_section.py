from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import organization, admin_staff, ADMIN_EMAIL, ADMIN_PASSWORD
import json

# imported serializer and model
from src.course.models import Section
from src.course.serializers import SectionSerializer
from src.course.models import Course


class TestSectionViewSet(APITestCase):
    def setUp(self):
        self.organization = organization("org")
        self.admin = admin_staff(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )

    def _create_course(self):
        return Course.objects.create(name="course", organization=self.organization)

    def _create_section(self):
        course = self._create_course()
        return Section.objects.create(name="class999", course=course)

    def test_create_section(self):
        url = "/api/v1/section/"
        course = self._create_course()
        data = {"name": "kodom2", "course": course.id}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data, format="json")
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)

    def test_retrieve_section(self):
        section = self._create_section()
        url = f"/api/v1/section/{section.id}/"
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        section_serializer_data = SectionSerializer(instance=section).data
        response_data = json.loads(response.content)
        self.assertEqual(section_serializer_data, response_data)

    def test_partial_update_section(self):
        section = self._create_section()
        self.client.force_authenticate(user=self.admin)
        url = f"/api/v1/section/{section.id}/"
        response = self.client.patch(url, {"name": "something"})
        response_data = json.loads(response.content)
        changed_section = Section.objects.get(id=section.id)
        self.assertEqual(response_data.get("name"), changed_section.name)

    def test_section_object_delete(self):
        section = self._create_section()
        self.client.force_authenticate(user=self.admin)
        url = f"/api/v1/section/{section.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
