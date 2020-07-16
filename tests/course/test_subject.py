from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
import json
from tests.course.conftest import course_object, teacher_object, subject_object
from src.course.models import Subject
from src.course.serializers import SubjectSerializer


class TestSubjectViewSet(APITestCase):
    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )
        self.course = course_object(self.organization.id)
        self.teacher = teacher_object("adilreza098@gmail.com")
        self.subject = subject_object("bangla",self.course, self.teacher)

    def test_create_section(self):
        url = "/api/v1/subject/"
        data = {"name": "bangla", "course": self.course.id, "teacher": self.teacher.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subject.objects.count(), 2)

    def test_retrieve_subject(self):
        url = f"/api/v1/subject/{self.subject.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        subject_serializer_data = SubjectSerializer(instance=self.subject).data
        response_data = json.loads(response.content)
        self.assertEqual(subject_serializer_data, response_data)

    def test_partial_update_course(self):
        url = f"/api/v1/subject/{self.subject.id}/"
        response = self.client.patch(url, {"name": "English"})
        response_data = json.loads(response.content)
        changed_subject = Subject.objects.get(id=self.subject.id)
        self.assertEqual(response_data.get("name"), changed_subject.name)

    def test_course_object_delete(self):
        url = f"/api/v1/subject/{self.subject.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)

