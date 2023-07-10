from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet, OrganizationViewSet, ProjectViewSet, SimpleProjectViewSet,
    ProjectCreateViewSet, AddUserToProjectViewSet, TasksViewSet, CommentViewSet
)


app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('tasks', TasksViewSet, basename='tasks')
router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'organizations',
        OrganizationViewSet.as_view({'get': 'list', 'post': 'create'}),
    ),
    path(
        'organizations/(<int:pk>/', OrganizationViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}
        ),
    ),
    path(
        'organizations/<int:pk>/users/<int:user_id>/',
        OrganizationViewSet.as_view({'delete': 'destroy', 'put': 'update'})
    ),
    path(
        'users/<int:id>/projects/',
        ProjectViewSet.as_view({'get': 'list'}),
    ),
    path(
        'organizations/<int:organization_id>/projects/',
        ProjectCreateViewSet.as_view(
            {'post': 'create'}
        )
    ),
    path(
        'projects/<int:project_id>',
        SimpleProjectViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}
        ),
    ),
    path(
        ('projects/<int:project_id>'
            '/users/<int:user_id>/'),
        AddUserToProjectViewSet.as_view(
            {'put': 'update'}
        ),
    ),
]
