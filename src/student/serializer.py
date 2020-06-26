from rest_framework import  serializers

# imported model
from .models import  Student,FinancialInfo, GuardianInfo

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ["date_created","last_updated"]

class FinancialInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialInfo
        fields = "__all__"

class GuardianInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuardianInfo
        exclude = ["is_staff","is_admin_staff","is_academic","organization","date_joined","is_active","password","last_login","is_superuser","groups","user_permissions"]