from django.db import models
from source.auth_service.models import User
# Create your models here.

class Club(models.Model):
    club_head = models.ForeignKey(User,on_delete=models.PROTECT,related_name='head')
    club_name = models.CharField(max_length=50)
    description=models.CharField(max_length=50)
    club_logo=models.ImageField()
    club_members = models.ManyToManyField(User,related_name='members')


class ClubNews(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    
    

class ClubPost(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='posts')
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title    