from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from tasks.models import Comment, OrganizationUser, ProjectUser


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


class BaseCommentPermission(IsAuthenticated):
    role = None

    def has_object_permission(self, request, view, obj):
        comment_id = view.kwargs.get('pk')
        project = Comment.objects.get(pk=comment_id).task.project
        try:
            project_user = ProjectUser.objects.get(
                project_id=project,
                user=request.user,
            )
        except ObjectDoesNotExist:
            return False
        return project_user.role == self.role


class IsProjectManagerComment(BaseCommentPermission):
    role = ProjectUser.PROJECT_MANAGER


class IsBaseUserComment(BaseCommentPermission):
    role = ProjectUser.BASE_USER


class IsObserverComment(BaseCommentPermission):
    role = ProjectUser.OBSERVER

    # def has_permission(self, request, view):
    #     if request.method == 'POST':
    #         return False
    #     return request.user.is_authenticated

    # def has_object_permission(self, request, view, obj):
    #     project_id = self.request.query_params.get('project_id')
    #     try:
    #         project_user = ProjectUser.objects.get(
    #             project_id=project_id,
    #             user=request.user,
    #         )
    #     except ObjectDoesNotExist:
    #         return False
    #     if request.method == 'GET':
    #         return project_user.role == self.role
    #     return False
