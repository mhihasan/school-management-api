
from src.student.models import Student,FinancialInfo, GuardianInfo

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

def financialinfo_object(student, amount):
    return FinancialInfo.objects.create(
        student=student,
        amount=amount,
        discount=5
    )

def guardian_info_object(student, email):
    return GuardianInfo.objects.create(
        student=student,
        email=email,
        phone="01774363237",
        is_guardian= True,
        relationship= "brother"
    )