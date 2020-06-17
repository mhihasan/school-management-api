from rest_framework import routers
from django.urls import path

# imported ViewSet
from .views import LegalInfoViewSet, LeaveViewSet
from .views import EmployeeViewSet

# generics view
from .views import LeaveByEmployee, LegalInfoByEmployee

router = routers.DefaultRouter()
router.register('',EmployeeViewSet),
router.register('leave', LeaveViewSet),
router.register('legalinfo', LegalInfoViewSet)

urlpatterns = [
    path('leavebyemployee/<int:id>', LeaveByEmployee.as_view()),
    path('legalinfobyemployee/<int:id>', LegalInfoByEmployee.as_view())
]+router.urls
