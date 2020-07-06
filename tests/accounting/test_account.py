import json

from rest_framework import status
from rest_framework.test import APITestCase

from src.accounting.models import Account
from src.accounting.serializers import AccountSerializer
from tests.conftest import (
    organization_object,
    admin_staff_object,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
)

from tests.accounting.conftest import account_object


class TestAccountViewSet(APITestCase):
    fixtures = ["account_group.json"]

    def setUp(self):
        self.organization = organization_object("org")
        self.admin = admin_staff_object(
            ADMIN_EMAIL, ADMIN_PASSWORD, org_id=self.organization.id
        )
        self.account = account_object(self.organization.id)

        self.client.force_authenticate(user=self.admin)

    def test_create_account_successfully(self):
        url = "/api/v1/accounts/?account_group=revenue"

        data = {"name": "Account1", "organization": self.organization.id}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(response.data["name"], "Account1")

    def test_retrieve_account(self):
        url = f"/api/v1/accounts/{self.account.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        account_serializer_data = AccountSerializer(instance=self.account).data
        response_data = json.loads(response.content)
        self.assertEqual(account_serializer_data, response_data)

    def test_list_accounts(self):
        url = "/api/v1/accounts/?account_group=revenue"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        resp = json.loads(response.content)
        self.assertEqual(len(resp["results"]), Account.objects.count())

        url = "/api/v1/accounts/?account_group=expense"
        response = self.client.get(url)
        resp = json.loads(response.content)
        self.assertEqual(len(resp["results"]), 0)

    def test_partial_update_account(self):
        url = f"/api/v1/accounts/{self.account.id}/"
        response = self.client.patch(url, {"name": "B"})
        response_data = json.loads(response.content)
        changed_account = Account.objects.get(id=self.account.id)
        self.assertEqual(response_data.get("name"), changed_account.name)

    def test_account_object_delete(self):
        url = f"/api/v1/accounts/{self.account.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
