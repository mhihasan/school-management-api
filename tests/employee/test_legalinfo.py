from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
import json
from src.employee.models import Employee, LegalInformation
from src.employee.serializer import LegalInformationSerializer
from .conftest import designation_object, employee_object, legalinfo_object


class TestLegalInfoViewSet(APITestCase):
    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )
        self.designation = designation_object("Lecturer", self.organization.id)
        self.employee = employee_object("adilreza7778@gmail.com")
        self.legalinfo = legalinfo_object(self.employee)
        self.client.force_authenticate(user=self.admin)

    def test_create_legalinfo(self):
        url = "/api/v1/employee/legalinfo/"
        data = {"employee": self.employee.id,
                "nid": "12123123123",
                "present_address": '[{"zilla":"kushtia"]',
                "permanent_address": '[{"zilla":"kushtia"}]',
                "additional_info": '[{"zilla":"kushtia"}]',
                }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LegalInformation.objects.count(), 2)

    def test_retrieve_legalinfo(self):
        url = f"/api/v1/employee/legalinfo/{self.legalinfo.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        legal_serializer_data = LegalInformationSerializer(instance=self.legalinfo).data
        response_data = json.loads(response.content)
        self.assertEqual(legal_serializer_data, response_data)

    def test_partial_update_legalinfo(self):
        url = f"/api/v1/employee/legalinfo/{self.legalinfo.id}/"
        response = self.client.patch(url, {"nid": "223444234233423"})
        response_data = json.loads(response.content)
        changed_legal = LegalInformation.objects.get(id=self.legalinfo.id)
        self.assertEqual(response_data.get("nid"), changed_legal.nid)

    def test_legalinfo_delete(self):
        url = f"/api/v1/employee/legalinfo/{self.legalinfo.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
