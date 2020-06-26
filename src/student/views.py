from rest_framework import viewsets
from src.user.models import User
from django.http import HttpResponse

# imported serializer
from .serializer import StudentSerializer, FinancialInfoSerializer, GuardianInfoSerializer

# imported Model
from .models import Student, FinancialInfo, GuardianInfo

# Create your views here.

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class FinancialInfoViewSet(viewsets.ModelViewSet):
    # queryset = FinancialInfo.objects.all()
    serializer_class = FinancialInfoSerializer
    queryset = FinancialInfo.objects.all()
    def get_queryset(self):
        queryset = self.queryset
        student = self.request.query_params.get('student','')
        if student:
            query_set = queryset.filter(student=student)
            return query_set
        else:
            return queryset
    

class GuardianInfoViewSet(viewsets.ModelViewSet):
    queryset = GuardianInfo.objects.all()
    serializer_class = GuardianInfoSerializer

    # def perform_create(self, request, *args, **kwargs):
    #     email = request.data["email"]
    #     username = email
    #     password = "Password123@"
    #     User.objects.create_user(email=email, password=password)
    #     serializer = GuardianInfoSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return HttpResponse({'message': "succefully saved"}, status=200)
