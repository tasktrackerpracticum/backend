from django.urls import include, path
from rest_framework.routers import SimpleRouter

import api.views as views

app_name = 'api'

router = SimpleRouter()

router.register('users', views.UserViewSet, basename='users')
router.register('projects', views.ProjectViewSet, basename='projects')
# router.register('projects/<int:project_id>/tasks', views.TasksViewSet, basename='tasks')


urlpatterns = [
    path('', include(router.urls)),
    path(
        'projects/<int:project_id>/users/<int:user_id>/',
        views.ProjectViewSet.as_view(
            {'delete': 'delete_user'}
        )
    ),
    path(
        'projects/<int:project_id>/tasks/', views.TasksViewSet.as_view(
            {'post': 'create'}
        )
    ),
    path(
        'projects/<int:project_id>/tasks/<int:task_id>/',
        views.TasksViewSet.as_view(
            {'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}
        )
    ),

]
# router.register('tasks', TasksViewSet, basename='tasks')
# router.register('organizations', OrganizationViewSet, basename='organizations')
#
# urlpatterns = [
#     path(
#         'tasks/<int:task_id>/comments/',
#         CommentViewSet.as_view({
#             'get': 'list', 'post': 'create'
#         })
#     ),
#     path(
#         'comments/<int:pk>/',
#         CommentViewSet.as_view({
#             'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
#         })
#     ),
#     path(
#         'projects/',
#         ProjectViewSet.as_view(
#             {'get': 'list'}
#         )
#     ),
#     path(
#         'projects/<int:project_id>/',
#         ProjectViewSet.as_view(
#             {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}
#         )
#     ),
#     path(
#         'organizations/<int:organization_id>/projects',
#         ProjectViewSet.as_view(
#             {'post': 'create'}
#         )
#     ),
#     path(
#         'tasks/<int:task_id>/users/<int:user_id>/',
#         TasksViewSet.as_view(
#             {'delete': 'user_delete'}
#         )
#     ),
#     path('', include(router.urls)),
# ]
