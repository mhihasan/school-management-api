from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
import json
from src.employee.models import Designation
from src.employee.serializer import DesignationSerializer
from .conftest import designation_object


class TestDesignationViewSet(APITestCase):
    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )

        self.client.force_authenticate(user=self.admin)
        self.designation = designation_object("Lecturer", self.organization.id)

    def test_create_designation(self):
        url = "/api/v1/employee/designation/"
        data = {"title": "Assistant Teacher",  "organization": self.organization.id}
        response = self.client.post(url, data, format="json")
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Designation.objects.count(), 2)
        self.assertEqual(response.data["title"], "Assistant Teacher")

    def test_retrieve_designation(self):
        url = f"/api/v1/employee/designation/{self.designation.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        designation_serializer_data = DesignationSerializer(instance=self.designation).data
        response_data = json.loads(response.content)
        self.assertEqual(designation_serializer_data, response_data)

    def test_partial_update_designation(self):
        url = f"/api/v1/employee/designation/{self.designation.id}/"
        response = self.client.patch(url, {"title": "lect"})
        response_data = json.loads(response.content)
        changed_desig = Designation.objects.get(id=self.designation.id)
        self.assertEqual(response_data.get("title"), changed_desig.title)

    def test_designation_delete(self):
        url = f"/api/v1/employee/designation/{self.designation.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
