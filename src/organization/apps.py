from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OrganizationAppConfig(AppConfig):
    name = "src.organization"
    verbose_name = _("Organization")
