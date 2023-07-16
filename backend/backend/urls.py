from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API documentation",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(
        template_name='admin/login.html',
    )),
    path('accounts/logout/', LogoutView.as_view(
        template_name='admin/logout.html',
    )),
    path('', include('djoser.urls.jwt')),
    path('', include("api.urls", namespace="api")),
    path(
        'api/docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='swagger-ui',
    ),
]
