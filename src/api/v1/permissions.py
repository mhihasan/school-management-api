from rest_framework import exceptions
from rest_framework.permissions import (
    DjangoModelPermissions,
    IsAuthenticated,
    BasePermission,
)

from src.user.utils import valid_staff


class ModelPermissions(DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


class IsStaff(IsAuthenticated):
    def has_permission(self, request, view):
        return valid_staff(request.user)


class IsAdminStaff(IsAuthenticated):
    def has_permission(self, request, view):
        return valid_staff(request.user, admin=True)


class IsSuperUser(IsAuthenticated):
    def has_permission(self, request, view):
        return valid_staff(request.user, superuser=True)


class BatchPostPermission(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.has_perm("accounting.post_batch") else False


class AuxiliaryModelPermission(BasePermission):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    authenticated_users_only = True

    def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        kwargs = {
            "app_label": model_cls._meta.app_label,
            "model_name": model_cls._meta.model_name,
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, "_ignore_model_permissions", False):
            return True

        if not request.user or (
            not request.user.is_authenticated and self.authenticated_users_only
        ):
            return False

        # permission checking for auxiliary model
        perms = self.get_required_permissions(request.method, view.auxiliary_model)

        return request.user.has_perms(perms)
