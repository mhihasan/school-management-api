from src.course.models import Course, Section, Subject
from src.employee.models import Employee


def course_object(org_id):
    return Course.objects.create(name="course", organization_id=org_id)


def section_object(course_id):
    return Section.objects.create(name="class999", course_id=course_id)


def teacher_object(email):
    return Employee.objects.create(email=email, first_name="teacher",gross_salary=89000)


def subject_object(name, course, teacher):
    return Subject.objects.create(name=name, course=course, teacher=teacher)
