from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    ProjectViewSet, UserViewSet, OrganizationViewSet,
    TasksViewSet, CommentViewSet
)


app_name = 'api'

router = SimpleRouter()

router.register(
    r'tasks/(?P<task_id>\d+)/comments', CommentViewSet, basename='comments')
router.register('users', UserViewSet, basename='users')
router.register('tasks', TasksViewSet, basename='tasks')
router.register('organizations', OrganizationViewSet, basename='organizations')
router.register('projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'organizations/<int:pk>/users/<int:user_id>/',
        OrganizationViewSet.as_view(
            {'delete': 'delete_user'}
        )
    ),
    path(
        'projects/<int:project_id>/users/<int:user_id>/',
        ProjectViewSet.as_view(
            {'delete': 'delete_user'}
        )
    ),
    path(
        'tasks/<int:task_id>/users/<int:user_id>/',
        TasksViewSet.as_view(
            {'delete': 'user_delete'}
        )
    )
]
