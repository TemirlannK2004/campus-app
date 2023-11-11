import re
from django.urls import reverse
from rest_framework import serializers
from . import models
from django.core.validators import EmailValidator
from django.contrib.auth import authenticate

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str,smart_bytes,force_str

from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed
from source.base.utils import send_resetPasswordLink_to_user

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = ['id','email','first_name','last_name']

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,min_length=8,write_only=True)
    re_password = serializers.CharField(max_length=68,min_length=8,write_only=True)
    email = serializers.EmailField(max_length=150,min_length=4)
    
    class Meta:
        model=models.User
        fields = ['id','email','first_name','last_name','password','re_password']    
    def validate(self, attrs):
        password=attrs.get('password','')
        re_password=attrs.get('re_password','')
        email = attrs.get('email','')
        email_validator = EmailValidator()

        if password!=re_password:
            raise serializers.ValidationError('Password Dont Match')
        
        try:
            email_validator(email)
        except ValueError:
            raise serializers.ValidationError('Invalid email address')
        
        return attrs


    
    def create(self,validated_data):
        user = models.User.objects.create_user(
            email=validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            password = validated_data['password']
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150,min_length=4)
    password = serializers.CharField(max_length=68,min_length=8,write_only=True)
    full_name = serializers.CharField(max_length = 150,read_only=True)
    last_name = serializers.CharField(max_length = 150,read_only=True)
    access_token = serializers.CharField(max_length=255,read_only=True)
    refresh_token = serializers.CharField(max_length=255,read_only=True)
    class Meta:
        model = models.User
        fields = ['email','password','full_name','last_name','access_token','refresh_token'] 

    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request,email=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials')
        user_token = user.tokens()

        return ({
            'email':user.email,
            'full_name':user.full_name,
            'last_name':user.last_name,
            'access_token':str(user_token.get('access')),
            'refresh_token':str(user_token.get('refresh')),
        })



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150,min_length=4)
    class Meta:
        fields = ['email']

    def validate(self,attrs):
        email = attrs.get('email')
        
        if models.User.objects.filter(email=email).exists():
            user = models.User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            request=self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link=reverse('password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
            abslink=f'http://{site_domain}{relative_link}'
            email_body=f'Hi! Reset Password link is here - {abslink}'
            data = {
                'email_body':email_body,
                'email_subject':'Reset Password',
                'to_email':user.email
            }

            send_resetPasswordLink_to_user(data)

            return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68,min_length=8,write_only=True)
    confirm_password =serializers.CharField(max_length=68,min_length=8,write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)


    class Meta:
        fields=['password','confirm_password','uidb64','token']

    def validate(self,attrs):
        try:
            password=attrs.get('token')
            confirm_password=attrs.get('confirm_password')
            uidb64=attrs.get('uidb64')
            token=attrs.get('token')


            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = models.User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('reset link is invalid or has expired',401)
            if password!=confirm_password:
                raise AuthenticationFailed('Passwords Dont Match')
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed('link is invalid or has expired',401)
            