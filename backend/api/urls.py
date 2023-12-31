from django.urls import include, path

from rest_framework.routers import SimpleRouter

import api.views as views

app_name = 'api'

router = SimpleRouter()

router.register('users', views.UserViewSet, basename='users')
router.register('projects', views.ProjectViewSet, basename='projects')
router.register('tasks', views.TasksViewSet, basename='tasks')

urlpatterns = [
    path(
        'projects/<int:project_id>/users/<int:user_id>/',
        views.ProjectViewSet.as_view({'delete': 'delete_user'}),
    ),
    path(
        'projects/<int:project_id>/tasks/',
        views.TasksViewSet.as_view({'post': 'create', 'get': 'list'}),
    ),
    path(
        'projects/<int:project_id>/tasks/<int:task_id>/',
        views.TasksViewSet.as_view(
            {'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'},
        ),
    ),
    path(
        'tasks/<int:task_id>/users/<int:user_id>/',
        views.TasksViewSet.as_view({'delete': 'delete_user'}),
    ),
    path(
        'tasks/<int:task_id>/comments/',
        views.CommentViewSet.as_view({'post': 'create', 'get': 'list'}),
    ),
    path(
        'comments/<int:pk>/',
        views.CommentViewSet.as_view(
            {'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'},
        ),
    ),
    path('tags/', views.TagViewSet.as_view({'get': 'list'})),
    path(
        'projects/<int:project_id>/tags/',
        views.TagViewSet.as_view({'post': 'create'}),
    ),
    path(
        'tags/<int:tag_id>/', views.TagViewSet.as_view({'delete': 'destroy'}),
    ),
    path('', include(router.urls)),
]
