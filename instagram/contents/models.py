from django.db import models

# Create your models here.
class Feed(models.Model) :
    content = models.TextField() #글 내용
    image = models.TextField() # 피드 이미지
    email = models.EmailField(default='') #글쓴이 이메일
    like_count = models.IntegerField() #좋아요 수

class Like(models.Model) :
    feed_id = models.IntegerField(default = 0)
    email = models.EmailField(default='') #글쓴이 이메일
    is_like = models.BooleanField(default=True) #좋아요 여부 : 취소하면 기록이 사라지지 않고 좋아요 여부가 N으로 바뀜

class Reply(models.Model) :
    feed_id = models.IntegerField(default = 0)
    email = models.EmailField(default='') #글쓴이 이메일
    reply_content = models.TextField()

class Bookmark(models.Model) :
    feed_id = models.IntegerField(default = 0)
    email = models.EmailField(default='') #글쓴이 이메일
    is_marked = models.BooleanField(default=True) #북마크 여부