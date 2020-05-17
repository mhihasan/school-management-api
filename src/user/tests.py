from rest_framework.test import APITestCase
from rest_framework import status
import json
from .models import Student
from tests.setup import create_org, create_admin


class StudentAPITest(APITestCase):
    def setUp(self):
        self.admin_username = "adilreza"
        self.password = "12345"
        self.organization = create_org("org")
        self.admin = create_admin(
            self.admin_username, self.password, org_id=self.organization.id
        )

    def _create_student(self):
        return Student.objects.create(
            name="Adil Reza",
            birth_date="2019-05-04",
            father_name="bakul Ali",
            present_address=[
                {
                    "village": "baggaripara",
                    "thana": "Bheramara",
                    "zilla": "kusthtia",
                    "aditional": "here extra info",
                }
            ],
            permanent_address=[
                {
                    "village": "baggaripara",
                    "thana": "Bheramara",
                    "zilla": "kusthtia",
                    "aditional": "here extra info",
                }
            ],
            guardian_information=[
                {
                    "name": "azmir hossain",
                    "relation": "brother",
                    "sub": "shihab islam",
                    "relation2": "brother",
                    "mobile": "01774363237",
                    "age": 30,
                }
            ],
            examiner_name="Azmal korim",
            result="result will be good excelent or anything else",
            admission_fee=2300,
            monthly_fee=4500,
            boarding_fee=340,
        )

    def test_add_student(self):
        data = {
            "username": "adilr",
            "password": "adilr356",
            "name": "Adil Reza",
            "birth_date": "2019-05-02",
            "father_name": "bakul Ali",
            "present_address": {
                "village": "baggaripara",
                "thana": "Bheramara",
                "zilla": "kusthtia",
                "aditional": "here will be all extra info",
            },
            "permanent_address": {
                "village": "baggaripara",
                "thana": "Bheramara",
                "zilla": "kusthtia",
                "aditional": "here will be all extra info",
            },
            "guardian_information": {
                "name": "azmir hossain",
                "relation": "brother",
                "sub": "shihab islam",
                "relation2": "brother",
                "mobile": "01774363237",
                "age": 30,
            },
            "examiner_name": "Azmal korim",
            "result": "result will be good excelent or anything else",
            "admission_fee": 2300,
            "monthly_fee": 4500,
            "boarding_fee": 340,
            "other_fees": {"book_buying": 4500, "initial_stay": 450, "extra": 430},
            "other_information": {
                "hobby": "gardenong",
                "fvrt_color": "red",
                "age": 5540,
            },
            "user": 1,
        }
        response = self.client.post("/api/v1/student/", data, format="json")
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_account(self):
        url = "/api/v1/student/"
        response = self.client.get(url)
        # json_data = json.loads(response.content)
        # print(json_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        student = self._create_student()
        url = "/api/v1/student/" + str(student.id) + "/"
        response = self.client.patch(
            url, {"examiner_name": "Nakib Hossain com"}, format="json"
        )
        self.assertEqual(
            json.loads(response.content)["examiner_name"], "Nakib Hossain com"
        )
