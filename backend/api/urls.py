from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet, OrganizationViewSet, ProjectViewSet,
)


app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet)
router.register(
    r'organizations/(?P<organizations_id>\d+)/projects',
    ProjectViewSet,
    basename='projects'
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'organizations',
        OrganizationViewSet.as_view({'get': 'list', 'post': 'create'})
    ),
    path(
        'organizations/<int:pk>/', OrganizationViewSet.as_view(
        {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})
    ),
    path(
        'organizations/<int:pk>/users/<int:user_id>/',
        OrganizationViewSet.as_view({'delete': 'destroy', 'put': 'update'})
    ),
]
