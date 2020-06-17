from rest_framework import routers

# imported ViewSet
from .views import CourseViewSet, CourseViewByOrganization, SubjectViewSet
from .views import SectionViewSet, AttendanceStudentViewSet, AttendanceTeacherViewSet

router = routers.DefaultRouter()

router.register('course', CourseViewSet),
router.register('subject', SubjectViewSet),
router.register('section', SectionViewSet),
router.register('attendance/student', AttendanceStudentViewSet),
router.register('attendance/teacher', AttendanceTeacherViewSet)

urlpatterns = router.urls