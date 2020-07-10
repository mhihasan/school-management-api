from src.course.models import Course, Section, Subject, Attendance
from src.employee.models import Employee
from src.student.models import Student


def course_object(org_id):
    return Course.objects.create(name="course", organization_id=org_id)


def section_object(course_id):
    return Section.objects.create(name="class999", course_id=course_id)


def teacher_object(email):
    return Employee.objects.create(email=email, first_name="teacher", gross_salary=89000)


def subject_object(name, course, teacher):
    return Subject.objects.create(name=name, course=course, teacher=teacher)

def attendance_object(teacher, student):
    return Attendance.objects.create(employee=teacher, student=student)

def student_object(section, org):
    return Student.objects.create(
        first_name="adill",
        last_name="rezaaa",
        roll_no="12312312312",
        section=section,
        present_address='[{"name": "kushtia"}]',
        permanent_address='[{"name": "kushtia"}]',
        additional_info='[{"name": "kushtia"}]',
        organization=org,
        gender=1,
    )
