"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import UploadFeed, Profile, UploadReply, ToggleLike, ToggleBookmark

urlpatterns = [
    path('content/upload', UploadFeed.as_view()),
    path('content/reply', UploadReply.as_view()),
    path('profile/', Profile.as_view()),
    path('content/like', ToggleLike.as_view()),
    path('content/bookmark', ToggleBookmark.as_view())
]