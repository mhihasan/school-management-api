from rest_framework import serializers

from .models import Employee
from .models import Leave, LegalInformation
from .models import Designation


class EmployeeSerializer(serializers.ModelSerializer):
    designation_name = serializers.SerializerMethodField("get_designation_name")
    class Meta:
        model = Employee
        fields = ("id", "first_name", "last_name","email", "is_admin_staff", "is_academic","employee_type",
                  "joining_date", "permanent_joining_date","gender", "birth_date", "blood_group", "gross_salary",
                  "photo", "organization", "designation","designation_name","sections")

    def get_designation_name(self, obj):
        title = str(obj.designation.title)
        return title


class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField("get_employee_name")
    class Meta:
        model = Leave
        fields = ["id","employee","employee_name","leave_type","days","start_date","end_date"]
    def get_employee_name(self, obj):
        f_name = obj.employee.first_name
        l_name = obj.employee.last_name
        emp_name = f_name+" "+l_name
        return emp_name


class LegalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalInformation
        fields = "__all__"


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = "__all__"
