from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    TasksUserDeleteViewSet, UserViewSet, OrganizationViewSet,
    SimpleProjectViewSet, AddUserToProjectViewSet,
    TasksViewSet, CommentViewSet
)


app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('tasks', TasksViewSet, basename='tasks')
router.register('comments', CommentViewSet, basename='comments')
router.register('organizations', OrganizationViewSet, basename='organizations')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'organizations/<int:pk>/users/<int:user_id>/',
        OrganizationViewSet.as_view(
            {'delete': 'delete_user'})
    ),
    path(
        'projects/<int:project_id>/',
        SimpleProjectViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}
        ),
    ),
    path(
        'projects/<int:project_id>/users/<int:user_id>/',
        AddUserToProjectViewSet.as_view(
            {'delete': 'destroy', 'put': 'update'}
        ),
    ),
    path(
        'tasks/<int:task_id>/users/<int:user_id>/',
        TasksUserDeleteViewSet.as_view(
            {'delete': 'destroy'}
        )
    )
]
