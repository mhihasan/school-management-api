from src.user.models import User


def valid_staff(user, superuser=False, admin=False):
    if not isinstance(user, User):
        return False
    if superuser:
        return user.is_superuser
    if admin:
        return user.is_admin_staff or user.is_superuser
    if user.organization is None:
        return False
    return True
