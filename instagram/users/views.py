from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class Join(APIView) :
    def get(self, request) :
        return render(request, "join.html")
    def post(self, request) :
        #TODO 회원가입
        pass

class LogIn(APIView) :
    def get(self, request) :
        return render(request, "login.html")
        #TODO 로그인
        pass