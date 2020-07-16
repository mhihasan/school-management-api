from src.organization.models import Organization
from src.user.models import User


def organization_object(name):
    return Organization.objects.create(name=name)


def admin_staff_object(email, password, org_id):
    return User.objects.create_user(
        email=email, password=password, is_admin_staff=True, organization_id=org_id,
    )


TEACHER_EMAIL, TEACHER_PASSWORD = "teacher@gmail.com", "teacher_password"
GUARDIAN_EMAIL, GUARDIAN_PASSWORD = "guardian@gmail.com", "guardian_password"
ADMIN_EMAIL, ADMIN_PASSWORD = "admin@gmail.com", "admin_password"
