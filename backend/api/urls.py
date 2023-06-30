from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, OrganizationViewSet, ProjectViewSet


app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet)
router.register('organizations', OrganizationViewSet, basename='organizations')
router.register(
    r'organizations/(?P<organizations_id>\d+)/projects',
    ProjectViewSet,
    basename='projects'
)

urlpatterns = [
    path('', include(router.urls)),
]
