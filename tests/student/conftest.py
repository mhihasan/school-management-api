
from src.student.models import Student

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
