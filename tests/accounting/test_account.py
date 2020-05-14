from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from src.accounting.models import Account
from src.organization.models import Organization
from src.user.models import User

client = APIClient()


def create_org(name):
    org = Organization(name=name)
    org.save()
    return org


def create_admin(username, password, org_id):

    admin_staff = User(
        username=username,
        password=password,
        is_admin_staff=True,
        organization_id=org_id,
    )
    admin_staff.set_unusable_password()
    admin_staff.save()
    return admin_staff


class TestAccountViewSet(APITestCase):
    fixtures = ["account_group.json"]

    def setUp(self):
        self.admin_username = "admin1"
        self.password = "password"
        self.organization = create_org("org")
        self.admin = create_admin(
            self.admin_username, self.password, org_id=self.organization.id
        )

    def test_create_account_successfully(self):
        url = "/api/v1/accounts/?account_group=revenue"

        data = {"name": "Account1", "organization": self.organization.id}
        client.force_authenticate(user=self.admin)
        response = client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, "Account1")
