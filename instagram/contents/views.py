from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed

# Create your views here.
class Main(APIView) :
    def get(self, request) :
        #select * from contents_feed → contents_feed에 있는 모든 데이터를 가져옴. 데이터는 역순(-id)
        feed_list=Feed.objects.all().order_by('-id') 

        return render(request, "main.html", context=dict(feeds=feed_list))