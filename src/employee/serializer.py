from rest_framework import serializers

# imported model 
from .models import Employee
from .models import Leave, LegalInformation
from .models import Designation

# Serializer 


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ("is_staff","is_active","is_guardian","password","last_login","is_superuser")


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ["employee","leave_type","days","start_date","end_date"]


class LegalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalInformation
        fields = "__all__"


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = "__all__"
