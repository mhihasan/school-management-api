from django.contrib import admin

from src.organization.models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "phone", "email"]
    exclude = ["date_created", "last_updated"]
    search_fields = ["name"]


admin.site.register(Organization, OrganizationAdmin)
