from django.shortcuts import render

from .serializers import UserSerializer,RegisterUserSerializer,LoginSerializer,PasswordResetRequestSerializer,SetNewPasswordSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import status
from .models import User,OneTimePasswordUser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from source.base.utils import send_code_to_user
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-joined_at')
    serializer_class = UserSerializer


class RegisterUserView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    def post(self,request):

        if User.objects.filter(email=request.data['email']).exists():
            return Response(
                {'error':'Email already used'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_code_to_user(email=serializer.data['email']) 
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


class VerifyUserEmail(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self,request):
        otp_code = request.data.get('otp_code')
        try:
            user_code = OneTimePasswordUser.objects.get(code=otp_code)
            user = user_code.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'message':'Your account has been verified successfully'},status=status.HTTP_200_OK
                )
            return Response({'message':'Code is invalid , user already verified'},status=status.HTTP_204_NO_CONTENT)
                
        except OneTimePasswordUser.DoesNotExist:
            return Response({'message':'Passcode Not exist'},status=status.HTTP_404_NOT_FOUND)    
        


class LoginView(APIView):
    def post(self,request):
        serializer_class = LoginSerializer     
        serializer = serializer_class(data=request.data,context = {'request':request})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self,request):
        serializer_class=PasswordResetRequestSerializer
        serializer = serializer_class(data = request.data,context = {'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':'A link has been success fully sended to ur email,Please check'})


class PasswordResetConfirm(APIView):
    def get(self,request,uidb64,token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'message':'token is invalid or has expired'},status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True,'message':'Valid Credentials','uidb64':uidb64,'token':token},status=status.HTTP_200_OK)
        
        except DjangoUnicodeDecodeError:
            return Response({'message':'token is invalid or has expired'},status=status.HTTP_401_UNAUTHORIZED)


class SetNewPassword(APIView):
    def patch(self,request):
        serializer_class = SetNewPasswordSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message':'password reset successfully '},status=status.HTTP_200_OK)




