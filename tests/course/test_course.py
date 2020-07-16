from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
from tests.course.conftest import course_object
import json

from src.course.models import Course
from src.course.serializers import CourseSerializer


class TestCourseViewSet(APITestCase):
    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )
        self.course = course_object(self.organization.id)

        self.client.force_authenticate(user=self.admin)

    def test_create_course(self):
        url = "/api/v1/course/"
        data = {"name": "class9", "organization": self.organization.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(response.data["name"], "class9")

    def test_retrieve_course(self):
        url = f"/api/v1/course/{self.course.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        course_serializer_data = CourseSerializer(instance=self.course).data
        response_data = json.loads(response.content)
        self.assertEqual(course_serializer_data, response_data)

    def test_partial_update_course(self):
        url = f"/api/v1/course/{self.course.id}/"
        response = self.client.patch(url, {"name": "B"})
        response_data = json.loads(response.content)
        changed_course = Course.objects.get(id=self.course.id)
        self.assertEqual(response_data.get("name"), changed_course.name)

    def test_course_object_delete(self):
        url = f"/api/v1/course/{self.course.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
