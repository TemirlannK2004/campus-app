from django.contrib import admin
from django.urls import path, include,re_path
from rest_framework import routers
from source.auth_service import views
from source.club_service import views
from django.conf import settings
import debug_toolbar
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Campus App DRF API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),

    path('api/v1/auth_service/', include('source.auth_service.urls')),
    path('api/v1/club_service/',include('source.club_service.urls')),
    path('api/v1/announcements_service/',include('source.announcements_service.urls')),


    path('api-auth/', include('rest_framework.urls')),
    path("__debug__/", include("debug_toolbar.urls")),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]


