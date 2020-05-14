from rest_framework.test import APIClient

from src.organization.models import Organization
from src.user.models import User

client = APIClient()


def create_org(name):
    org = Organization(name=name)
    org.save()
    return org


def create_admin(username, oid="org1"):
    org = create_org(oid)

    organizer = User(
        username=username,
        is_active=True,
        # role=ROLE_DICT['Organizer'],
        organization=org,
    )
    organizer.set_unusable_password()
    organizer.save()
    return organizer


#
#
# class TestAccountViewSet(APITestCase):
#     def setUp(self):
#         self.admin_username = "teacher1"
#         self.admin = create_admin(self.admin_username)

# def test_create_account(self):
#     url = "/api/v1/accounts/?account_group=revenue"
#     org = Organization.objects.create(name="test")
#     AccountGroup.objects.create(code=15, name="Revenue", category=9)
#
#     data = {"name": "DabApps"}
#     client.force_authenticate(user=self.admin)
#     response = self.client.post(url, data, format="json")
#     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     self.assertEqual(Account.objects.count(), 1)
#     self.assertEqual(Account.objects.get().name, "DabApps")
