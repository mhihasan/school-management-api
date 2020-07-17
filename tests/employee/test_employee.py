from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
import json
from src.employee.models import Employee
from src.employee.serializer import EmployeeSerializer
from .conftest import designation_object, employee_object


class TestEmployeeViewSet(APITestCase):
    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )
        self.designation = designation_object("Lecturer", self.organization.id)
        self.employee = employee_object("adilreza7778@gmail.com")
        self.client.force_authenticate(user=self.admin)

    def test_create_employee(self):
        url = "/api/v1/employee/"
        data = {"first_name": "adill", "last_name": "rezaaa", "email": "ad@gmail.com",
                "designation": self.designation.id,"gross_salary":98000
                }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.assertEqual(response.data["first_name"], "adill")

    def test_retrieve_employee(self):
        url = f"/api/v1/employee/{self.employee.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        employee_serializer_data = EmployeeSerializer(instance=self.employee).data
        response_data = json.loads(response.content)
        self.assertEqual(employee_serializer_data, response_data)

    def test_partial_update_employee(self):
        url = f"/api/v1/employee/{self.employee.id}/"
        response = self.client.patch(url, {"last_name": "ali"})
        response_data = json.loads(response.content)
        changed_employee = Employee.objects.get(id=self.employee.id)
        self.assertEqual(response_data.get("last_name"), changed_employee.last_name)

    def test_employee_delete(self):
        url = f"/api/v1/employee/{self.employee.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
