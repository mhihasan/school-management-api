import json

from rest_framework import status
from rest_framework.test import APITestCase

from src.accounting.models import Account
from src.accounting.serializers import AccountSerializer
from tests.conftest import organization, admin_staff, admin_credential


class TestAccountViewSet(APITestCase):
    fixtures = ["account_group.json"]

    def setUp(self):
        self.admin_email = admin_credential().get("email")
        self.password = admin_credential().get("password")
        self.organization = organization("org")
        self.admin = admin_staff(
            self.admin_email, self.password, org_id=self.organization.id
        )

    def _create_account(self):
        return Account.objects.create(
            name="a",
            group_id=15,
            balance_type=1,
            account_type=1,
            gl_code="xlg",
            organization_id=self.organization.id,
        )

    def test_create_account_successfully(self):
        url = "/api/v1/accounts/?account_group=revenue"

        data = {"name": "Account1", "organization": self.organization.id}
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, "Account1")

    def test_retrieve_account(self):
        account = self._create_account()
        url = f"/api/v1/accounts/{account.id}/"
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        account_serializer_data = AccountSerializer(instance=account).data
        response_data = json.loads(response.content)
        self.assertEqual(account_serializer_data, response_data)

    def test_list_accounts(self):
        self._create_account()
        url = "/api/v1/accounts/?account_group=revenue"
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        resp = json.loads(response.content)
        self.assertEqual(len(resp["results"]), Account.objects.count())

        url = "/api/v1/accounts/?account_group=expense"
        response = self.client.get(url)
        resp = json.loads(response.content)
        self.assertEqual(len(resp["results"]), 0)

    def test_partial_update_account(self):
        account = self._create_account()
        self.client.force_authenticate(user=self.admin)
        url = f"/api/v1/accounts/{account.id}/"
        response = self.client.patch(url, {"name": "B"})
        response_data = json.loads(response.content)
        changed_account = Account.objects.get(id=account.id)
        self.assertEqual(response_data.get("name"), changed_account.name)

    def test_account_object_delete(self):
        account = self._create_account()
        self.client.force_authenticate(user=self.admin)
        url = f"/api/v1/accounts/{account.id}/"
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
