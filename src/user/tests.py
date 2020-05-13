
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
import json
from .models import Student
import datetime

# Create your tests here.

class StudentAPITest(APITestCase):
        # def setUp(self):
        #     Student.objects.create(
        #         name="Adil Reza",
        #         birth_date=datetime.date.today,
        #         father_name="bakul Ali",
        #         present_address =[{"village":"baggaripara","thana":"Bheramara","zilla":"kusthtia","aditional":"here extra info"}],
        #         permanent_address=[{"village":"baggaripara","thana":"Bheramara","zilla":"kusthtia","aditional":"here extra info"}],
        #         guardian_information=[{
        #             "name":"azmir hossain",
        #             "relation":"brother",
        #             "sub":"shihab islam",
        #             "relation2":"brother",
        #             "mobile":"01774363237",
        #             "age":30
        #         }],
        #         examiner_name="Azmal korim",
        #         result="result will be good excelent or anything else",
        #         admission_fee = 2300,
        #         monthly_fee = 4500,
        #         boarding_fee = 340,
        #         other_fees = [{"book_buying":4500,"initial_stay":450,"extra":430}]
                
        #     )
        def test_add_student(self):
            data = {
                "name": "Adil Reza",
                "birth_date": datetime.date.today,
                "father_name": "bakul Ali",
                "present_address":[{"village":"baggaripara","thana":"Bheramara","zilla":"kusthtia","aditional":"here will extra info"}],
                "permanent_address":[{"village":"baggaripara","thana": "Bheramara","zilla":"kusthtia"}],
                "guardian_information": [{
                    "name": "azmir hossain",
                    "relation": "brother",
                    "sub": "shihab islam",
                    "relation2": "brother",
                    "mobile": "01774363237",
                    "age": 30
                }],
                "examiner_name": "Azmal korim",
                "result": "result will be good excelent or anything else",
                "admission_fee": 2300,
                "monthly_fee": 4500,
                "boarding_fee": 340,
                "other_fees" :[{"book_buying":4500,"initial_stay":450,"extra":430}],
                "other_information": [{"hobby":"gardenong","fvrt_color":"red"}]
            }

            response = self.client.post("/api/v1/student/", data)
            print(response)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
