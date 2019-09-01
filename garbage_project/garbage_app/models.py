from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    Desciption=models.CharField(max_length=200)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    post_date=models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.Desciption


class Vote(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    voted_by=models.ForeignKey(User,on_delete=models.CASCADE)

    