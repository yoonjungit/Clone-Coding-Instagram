from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password

# Create your views here.
class Join(APIView) :
    def get(self, request) :
        return render(request, "join.html")
    def post(self, request) :
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email = email, nickname=nickname, name=name, password=make_password(password))
        return Response(status=200)

class LogIn(APIView) :
    def get(self, request) :
        return render(request, "login.html")

    def post(self, request) :
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        #리스트 형태로 반환, 가장 첫번째 요소first()를 user로 지정
        user = User.objects.filter(email = email).first()

        #가입되지 않은 이메일인 경우
        if user is None :
            return Response(status = 404, data = dict(message = "회원 정보가 잘못되었습니다."))
        #비밀번호가 맞는 경우
        if user.check_password(password) :
            request.session['email'] = email
            return Response(status=200)
        #비밀번호가 틀린 경우
        else : 
            return Response(status= 400, data = dict(message = "회원 정보가 잘못되었습니다."))
        #이메일, 비밀번호 오류인 경우 둘다 똑같은 메세지를 보여준다.