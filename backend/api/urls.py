from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CommentViewSet, OrganizationViewSet, ProjectViewSet,
                    TasksViewSet, UserViewSet)

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet, basename='users')
router.register('tasks', TasksViewSet, basename='tasks')
router.register('organizations', OrganizationViewSet, basename='organizations')
router.register('projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path(
        'tasks/<int:task_id>/comments/',
        CommentViewSet.as_view({
            'get': 'list', 'post': 'create'
        })
    ),
    path(
        'comments/<int:pk>/',
        CommentViewSet.as_view({
            'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
        })
    ),
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
    ),
    path('', include(router.urls)),
]
