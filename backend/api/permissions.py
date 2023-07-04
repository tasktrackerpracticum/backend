from rest_framework import permissions

from users.models import User
from tasks.models import Organization, OrganizationUser


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        ids = []
        for user in obj.users.all():
            org_user = OrganizationUser.objects.get(organization=obj, user=user)
            if org_user.role == 'создатель':
                ids.append(user.id)
        return (
            request.method in permissions.SAFE_METHODS and request.user.is_authenticated
            or request.user.id in ids
        )


class IsProjectOrCreatorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        organization = request.resolver_match.kwargs.get('organization')
        organization = Organization.objects.get(id=organization)
        try:
            org_user = OrganizationUser.objects.get(organization=organization, user=request.user)
        except:
            return False
        return (request.method == 'POST' and org_user.role == 'создатель') or request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        organization = request.resolver_match.kwargs.get('organization')
        organization = Organization.objects.get(id=organization)
        try:
            org_user = OrganizationUser.objects.get(organization=organization, user=request.user)
        except:
            return False
        return request.method == 'GET' or org_user.role in ('создатель', 'ПМ')
