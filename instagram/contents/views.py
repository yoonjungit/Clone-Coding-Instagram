from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Feed, Reply, Like, Bookmark
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

        #세션 정보(이메일)
        email = request.session.get('email', None)

        # 예외(1) 로그인을 안한 경우
        if email is None :
            return render(request, "login.html")
            
        user = User.objects.filter(email=email).first()

        # 예외(2) 로그인에 실패한 경우(아이디, 비밀번호 오류)
        if user is None :
            return render(request, "login.html")


        for feed in feed_object_list :
            user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id = feed.id)
            reply_list = []
            for reply in reply_object_list :
                user = User.objects.filter(email=feed.email).first()
                reply_user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content, reply_nickname = reply_user.nickname))
            
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked = Like.objects.filter(feed_id=feed.id, email = email, is_like=True).exists()
            is_marked = Bookmark.objects.filter(feed_id=feed.id, email = email, is_marked=True).exists()
            
            feed_list.append(dict(id = feed.id, image=feed.image, content = feed.content,
                                    profile_img=user.profile_img, reply_list = reply_list, 
                                    reply_nickname = reply_user.nickname, nickname = user.nickname,
                                    like_count=like_count, is_liked = is_liked, is_marked = is_marked))
        
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

class UploadReply(APIView) :
    def post(self, request) :
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)

class ToggleLike(APIView) :
    def post(self, request) :
        feed_id = request.data.get('feed_id', None)
        is_like = request.data.get('is_like', None)

        if is_like == "false" :
            is_like = True
        else : 
            is_like = False
        
        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()
        if like :
            like.is_like = is_like
            like.save()
        else : 
            Like.objects.create(feed_id=feed_id, is_like = is_like , email=email)

        return Response(status=200)

class ToggleBookmark(APIView) :
    def post(self, request) :
        feed_id = request.data.get('feed_id', None)
        is_marked = request.data.get('is_marked', None)

        if is_marked == "false" :
            is_marked = True
        else : 
            is_marked = False
        
        email = request.session.get('email', None)

        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()
        if bookmark :
            bookmark.is_marked = is_marked
            bookmark.save()
        else : 
            Bookmark.objects.create(feed_id=feed_id, is_marked = is_marked , email=email)

        return Response(status=200)