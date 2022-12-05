from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Feed
from uuid import uuid4
import os
from instagram.settings import MEDIA_ROOT
from users.models import User

#위 settings에서 urls.py에서 잘못 세팅해서 오류가 났었음

# Create your views here.
class Main(APIView) :
    def get(self, request) :
        #select * from contents_feed → contents_feed에 있는 모든 데이터를 가져옴. 데이터는 역순(-id)
        feed_object_list=Feed.objects.all().order_by('-id')
        feed_list = []

        for feed in feed_object_list :
            user = User.objects.filter(email=feed.email).first()
            feed_list.append(dict(image=feed.image, content = feed.content, like_count=feed.like_count, profile_img=user.profile_img, nickname=user.nickname))
        
        email = request.session.get('email', None)

        # 예외(1) 로그인을 안한 경우
        if email is None :
            return render(request, "login.html")
            
        user = User.objects.filter(email=email).first()

        # 예외(2) 로그인에 실패한 경우(아이디, 비밀번호 오류)
        if user is None :
            return render(request, "login.html")

        return render(request, "main.html", context=dict(feeds=feed_list, user=user))

class UploadFeed(APIView) :
    def post(self, request) :
        # 파일 불러오기
        file = request.FILES['file']
        # 파일 이름 랜덤 저장(한글 에러 방지)
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        file = uuid_name
        content = request.data.get('content')
        email = request.session.get('email', None)

        Feed.objects.create(image = file, content = content, email=email, like_count=0)

        return Response(status = 200 )
        
class Profile(APIView) :
    def get (self, request) :
        feed_list=Feed.objects.all().order_by('-id') 

        email = request.session.get('email', None)

        # 예외(1) 로그인을 안한 경우
        if email is None :
            return render(request, "login.html")
            
        user = User.objects.filter(email=email).first()

        # 예외(2) 로그인에 실패한 경우(아이디, 비밀번호 오류)
        if user is None :
            return render(request, "login.html")

        return render(request, "profile.html", context=dict(user=user))