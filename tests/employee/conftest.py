from src.employee.models import Designation, Employee, Leave


def designation_object(title, org_id):
    return Designation.objects.create(title=title, organization_id=org_id)


def employee_object(email):
    return Employee.objects.create(email=email, first_name="teacher", gross_salary=89000)


def leave_object(employee):
    return Leave.objects.create(
        employee=employee,
        leave_type=1,
        days=50,
        start_date="2020-04-05",
        end_date="2020-04-10"
    )

