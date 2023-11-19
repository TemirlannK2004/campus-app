from django.db import models
from source.auth_service.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=2000)
    pass