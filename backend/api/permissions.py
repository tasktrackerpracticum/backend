from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from tasks.models import Organization, OrganizationUser, ProjectUser


class BaseRoleOrganizationPermission(IsAuthenticated):
    role = None

    def has_object_permission(self, request, view, obj):
        if obj.users.filter(id=request.user.id).exists():
            role = OrganizationUser.objects.get(
                user=request.user,
                organization=obj
            ).role
            return (False
                    if role == OrganizationUser.FORBIDDEN
                    else role == self.role)
        return False


class BaseProjectPermission(IsAuthenticated):
    role = None

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        try:
            project_user = ProjectUser.objects.get(
                project=obj,
                user=request.user,
            )
        except ObjectDoesNotExist:
            return False
        return project_user.role == self.role


class IsProjectManager(BaseProjectPermission):
    role = ProjectUser.PROJECT_MANAGER


class IsOrganizationCreator(BaseRoleOrganizationPermission):
    role = OrganizationUser.CREATOR


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class BaseTaskPermission(IsAuthenticated):
    role = None

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        try:
            project_user = ProjectUser.objects.get(
                project=obj.project,
                user=request.user,
            )
        except ObjectDoesNotExist:
            return False
        return project_user.role == self.role


class IsProjectManagerTask(BaseTaskPermission):
    role = ProjectUser.PROJECT_MANAGER


class IsBaseUserTask(BaseTaskPermission):
    role = ProjectUser.BASE_USER


class IsObserverTask(BaseTaskPermission):
    role = ProjectUser.OBSERVER

    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        try:
            project_user = ProjectUser.objects.get(
                project=obj.project,
                user=request.user,
            )
        except ObjectDoesNotExist:
            return False
        if request.method == 'GET':
            return project_user.role == self.role
        return False
