from django.db import models

# Create your models here.
class Feed(models.Model) :
    content = models.TextField() #글 내용
    image = models.TextField() # 피드 이미지
    email = models.EmailField(default='') #글쓴이 이메일
    like_count = models.IntegerField() #좋아요 수