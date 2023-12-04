from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core import validators

from django.utils.translation import gettext_lazy as _
from source.base.user_management import CustomUserManager
from source.base.service import validate_size_image
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken


# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=150,unique=True,verbose_name=_('Email Address'),validators=[validators.EmailValidator('That email can’t be used')])
    first_name = models.CharField(max_length=100,verbose_name=_('First name')   )
    last_name = models.CharField(max_length=100,verbose_name=_('Last Name'))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    avatar = models.ImageField(
        upload_to='user_avatars/',
        blank=True,
        null=True,
        validators=[validators.FileExtensionValidator(allowed_extensions=['png','jpg','jpeg']),validate_size_image]
    )

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=['first_name','last_name'] 
    objects=CustomUserManager()

    def __str__(self: str)-> str:
        return self.email
    
    @property
    def full_name(self: str)-> str:
        return f'{self.first_name} {self.last_name}'
    
    def tokens(self: str)-> str:
        refresh = RefreshToken.for_user(self)
        return ({
                'refresh':str((refresh)),
                'access':str(refresh.access_token),                   
                }) 
    


class OneTimePasswordUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=6,unique=True)

    def __str__(self: str)-> str:
        return self.user.first_name % 'passcode'
    