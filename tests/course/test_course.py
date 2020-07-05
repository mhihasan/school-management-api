from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import organization, admin_staff, admin_credential
import json

# imported serializer and model
from src.course.models import Course
from src.course.serializers import CourseSerializer


class TestCourseViewSet(APITestCase):

    def setUp(self):
        self.admin_email = admin_credential().get("email")
        self.password = admin_credential().get("password")
        self.organization = organization("org")
        self.admin = admin_staff(
            self.admin_email, self.password, org_id=self.organization.id
        )

    def _create_course(self):
        #data = {'name' 'class9',"organization":self.organization.id}
        return Course.objects.create(
            name="class999",
            organization=self.organization
        )


    def test_create_course(self):
        url = "/api/v1/course/"
        data = {'name': 'class9',"organization":self.organization.id}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().name, 'class9')

    def test_retrieve_course(self):
        course = self._create_course()
        url = f"/api/v1/course/{course.id}/"
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        course_serializer_data = CourseSerializer(instance=course).data
        response_data = json.loads(response.content)
        self.assertEqual(course_serializer_data, response_data)

    def test_partial_update_course(self):
        course = self._create_course()
        self.client.force_authenticate(user=self.admin)
        url = f"/api/v1/course/{course.id}/"
        response = self.client.patch(url, {"name": "B"})
        response_data = json.loads(response.content)
        changed_course = Course.objects.get(id=course.id)
        self.assertEqual(response_data.get("name"), changed_course.name)

    def test_course_object_delete(self):
        course = self._create_course()
        self.client.force_authenticate(user=self.admin)
        url = f"/api/v1/course/{course.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)

