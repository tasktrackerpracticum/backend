from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from tasks.models import Comment, ProjectUser


class BaseProjectPermission(IsAuthenticated):
    """Base abstract project permission."""

    role = None

    def has_permission(self, request, view):
        """Check if user has permission to GET request."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if user has rights to change object."""
        project_user = ProjectUser.objects.filter(
            project=obj, user=request.user,
        )
        return project_user.exists() and project_user[0].role == self.role


class IsProjectManager(BaseProjectPermission):
    """Check that user is project manager on project."""

    role = ProjectUser.PROJECT_MANAGER


class IsSelf(permissions.BasePermission):
    """Check that user is creator of object."""

    def has_object_permission(self, request, view, obj):
        """Check if user has rights to change object."""
        return request.user == obj


class BaseTaskPermission(IsAuthenticated):
    """Abstract base Task permission class."""

    role = None

    def has_object_permission(self, request, view, obj):
        """Check if user has rights to change object."""
        project_user = ProjectUser.objects.filter(
            project=obj, user=request.user,
        )
        return project_user.exists() and project_user[0].role == self.role


class IsProjectManagerTask(BaseTaskPermission):
    """Check that user is project manager on project."""

    role = ProjectUser.PROJECT_MANAGER


class IsBaseUserTask(BaseTaskPermission):
    """Check that user is base user on project."""

    role = ProjectUser.BASE_USER


class IsObserverTask(BaseTaskPermission):
    """Check that user is observer on project."""

    role = ProjectUser.OBSERVER

    def has_permission(self, request, view):
        """Check if user has permission to GET request."""
        if request.method == 'POST':
            return False
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if user has rights to change object."""
        project_user = ProjectUser.objects.filter(
            project=obj, user=request.user,
        )
        if project_user.exists() and request.method == 'GET':
            return project_user[0].role == self.role
        return False


class BaseCommentPermission(IsAuthenticated):
    """Abstract base Comment permission class."""

    role = None

    def has_object_permission(self, request, view, obj):
        """Check if user has rights to change object."""
        comment_id = view.kwargs.get('pk')
        project = Comment.objects.get(pk=comment_id).task.project
        project_user = ProjectUser.objects.filter(
            project=project, user=request.user,
        )
        return project_user.exists() and project_user[0].role == self.role


class IsProjectManagerComment(BaseCommentPermission):
    """Check that user is project manager on project."""

    role = ProjectUser.PROJECT_MANAGER


class IsBaseUserComment(BaseCommentPermission):
    """Check that user is base user on project."""

    role = ProjectUser.BASE_USER


class IsObserverComment(BaseCommentPermission):
    """Check that user is observer on project."""

    role = ProjectUser.OBSERVER


class TagPermission(IsAuthenticated):
    """Check permission to tag model for user."""

    def has_object_permission(self, request, view, obj):
        """Check if user has rights to change object."""
        return obj.user == request.user
