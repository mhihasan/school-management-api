from src.organization.models import Organization
from src.user.models import User


def create_org(name):
    org = Organization(name=name)
    org.save()
    return org


def create_admin(username, password, org_id):
    return User.objects.create_user(
        username=username,
        password=password,
        is_admin_staff=True,
        organization_id=org_id,
    )
