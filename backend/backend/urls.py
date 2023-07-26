from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Task Tracker",
        default_version="v1",
        description="""API documentation for Task Tracker project.
        Made by graduates of Yandex Practikum school.
        <a href="https://t.me/catstyle1101" target="_blank">Anton Masyuk</a>\
        and <a href="https://t.me/K0nstantin8891" target="_blank">\
        Konstantin Vasilyev</a>""",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook/', include('bot.urls', namespace='bot')),
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

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
