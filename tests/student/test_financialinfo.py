from rest_framework import status
from rest_framework.test import APITestCase
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)
from tests.student.conftest import student_object,financialinfo_object
from tests.course.conftest import course_object, section_object
import json

# imported serializer and model
from src.student.models import FinancialInfo

from src.student.serializer import FinancialInfoSerializer


class TestFinancialInfoViewSet(APITestCase):
    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )
        self.course = course_object(self.organization.id)
        self.section = section_object(self.course.id)
        self.student = student_object(self.section, self.organization)
        self.financial_info = financialinfo_object(self.student, 5000)
        self.client.force_authenticate(user=self.admin)


    def test_create_financialinfo(self):
        url = "/api/v1/student/financialinfo/"
        data = {
                "student":self.student.id,
                "amount": 1200,
                "discount": 5,
        }
        response = self.client.post(url, data, format="json")
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FinancialInfo.objects.count(), 2)
        self.assertEqual(response.data["student"], self.student.id)

    def test_retrieve_financial_info(self):
        url = f"/api/v1/student/financialinfo/{self.financial_info.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        financial_info_serializer_data = FinancialInfoSerializer(instance=self.financial_info).data
        response_data = json.loads(response.content)
        self.assertEqual(financial_info_serializer_data, response_data)

    def test_partial_update_financial_info(self):
        url = f"/api/v1/student/financialinfo/{self.financial_info.id}/"
        response = self.client.patch(url, {"amount": "1300"})
        response_data = json.loads(response.content)
        changed_data = FinancialInfo.objects.get(id=self.financial_info.id)
        self.assertEqual(response_data.get("amount"), str(changed_data.amount))


    def test_account_object_delete(self):
        url = f"/api/v1/student/financialinfo/{self.financial_info.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)

