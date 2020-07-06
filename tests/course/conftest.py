from src.course.models import Course, Section


def course_object(org_id):
    return Course.objects.create(name="course", organization_id=org_id)


def section_object(course_id):
    return Section.objects.create(name="class999", course_id=course_id)
