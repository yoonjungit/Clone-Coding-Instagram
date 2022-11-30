from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
    """
        user profile photo
        user nickname(id) 
        user name : 실제 사용자 이름
        user email
        user password : 디폴트 값
    """
    profile_img = models.TextField()
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email=models.EmailField(unique=True)
    USERNAME_FIELD = 'nickname'

class Meta :
    db_table = "User"
