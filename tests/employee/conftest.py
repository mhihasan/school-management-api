from src.employee.models import Designation


def designation_object(title, org_id):
    return Designation.objects.create(title=title, organization_id=org_id)
