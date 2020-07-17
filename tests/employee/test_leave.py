from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
import json
from src.employee.models import Leave
from src.employee.serializer import LeaveSerializer
from .conftest import designation_object, employee_object, leave_object


class TestLeaveViewSet(APITestCase):
    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )
        self.designation = designation_object("Lecturer", self.organization.id)
        self.employee = employee_object("adilreza7778@gmail.com")
        self.leave = leave_object(self.employee)
        self.client.force_authenticate(user=self.admin)

    def test_create_leave(self):
        url = "/api/v1/employee/leave/"
        data = {"employee": self.employee.id,
                "leave_type": 1,
                "days": 5,
                "start_date": "2020-04-05",
                "end_date": "2020-04-10"
            }
        response = self.client.post(url, data, format="json")
        print
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Leave.objects.count(), 2)

    def test_retrieve_leave(self):
        url = f"/api/v1/employee/leave/{self.leave.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        leave_serializer_data = LeaveSerializer(instance=self.leave).data
        response_data = json.loads(response.content)
        self.assertEqual(leave_serializer_data, response_data)

    def test_partial_update_leave(self):
        url = f"/api/v1/employee/leave/{self.leave.id}/"
        response = self.client.patch(url, {"days": 10})
        response_data = json.loads(response.content)
        changed_leave = Leave.objects.get(id=self.leave.id)
        self.assertEqual(response_data.get("days"), changed_leave.days)

    def test_leave_delete(self):
        url = f"/api/v1/employee/leave/{self.leave.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
