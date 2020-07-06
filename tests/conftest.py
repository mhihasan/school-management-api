from src.organization.models import Organization
from src.user.models import User


def organization(name):
    org = Organization(name=name)
    org.save()
    return org


def admin_staff(email, password, org_id):
    return User.objects.create_user(
        email=email, password=password, is_admin_staff=True, organization_id=org_id,
    )


def admin_credential():
    return {"email": "adilreza043@gmail.com", "password": "Adilreza043@"}


def teacher_email():
    return "teacher@gmail.com"


def guardian_email():
    return "guardian@gmail.com"


ADMIN_EMAIL, ADMIN_PASSWORD = (
    "adilreza043@gmail.com",
    "Adilreza043@",
)
