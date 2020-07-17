from src.employee.models import Designation, Employee


def designation_object(title, org_id):
    return Designation.objects.create(title=title, organization_id=org_id)


def employee_object(email):
    return Employee.objects.create(email=email, first_name="teacher", gross_salary=89000)