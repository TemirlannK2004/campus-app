from django.urls import path, include
from source.auth_service import views
from rest_framework import routers

from rest_framework_simplejwt.views import (    TokenObtainPairView,    TokenRefreshView,)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/',views.RegisterUserView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain-pair'),    
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('verify_email/', views.VerifyUserEmail.as_view(), name='verify-email'),

    path('password-reset/',views.PasswordResetRequestView.as_view(),name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/',views.PasswordResetConfirm.as_view(),name='password-reset-confirm'),
    path('set-new-password/',views.SetNewPassword.as_view(),name='set-new-password'),

    
]
