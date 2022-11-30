from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Feed
from uuid import uuid4
import os
from instagram.settings import MEDIA_ROOT
#위 settings에서 urls.py에서 잘못 세팅해서 오류가 났었음

# Create your views here.
class Main(APIView) :
    def get(self, request) :
        #select * from contents_feed → contents_feed에 있는 모든 데이터를 가져옴. 데이터는 역순(-id)
        feed_list=Feed.objects.all().order_by('-id') 

        return render(request, "main.html", context=dict(feeds=feed_list))

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
        image = request.data.get('image')
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        Feed.objects.create(image = file, content = content, user_id = user_id, profile_image=profile_image, like_count=0)

        return Response(status = 200 )