from src.course.models import Course


def course_object(self, org_id):
    return Course.objects.create(name="course", organization=org_id)
