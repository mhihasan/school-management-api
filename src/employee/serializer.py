from rest_framework import serializers

# imported model 
from .models import Employee
from .models import Leave, LegalInformation

# Serializer 

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "email","is_academic","is_admin_staff","designation",
        "employee_type","joining_date","permanent_joining_date","sections","gender","birth_date","blood_group",
        "gross_salary","photo"]

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ["employee","leave_type","days","start_date","end_date"]

class LegalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalInformation
        fields = "__all__"