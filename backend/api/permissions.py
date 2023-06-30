from rest_framework import permissions

from users.models import User
from tasks.models import Organization, OrganizationUser


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        ids = []
        for user in obj.users.all():
            org_user = OrganizationUser.objects.get(organization_id=obj, user_id=user)
            if org_user.role == 'создатель':
                ids.append(user.id)
        return (
            request.method in permissions.SAFE_METHODS and request.user.is_authenticated
            or request.user.id in ids
        )


class IsProjectOrCreatorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        organization_id = request.resolver_match.kwargs.get('organization_id')
        organization = Organization.objects.get(id=organization_id)
        try:
            org_user = OrganizationUser.objects.get(organization_id=organization, user_id=request.user)
        except:
            return False
        return (request.method == 'POST' and org_user.role == 'создатель') or request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        organization_id = request.resolver_match.kwargs.get('organization_id')
        organization = Organization.objects.get(id=organization_id)
        try:
            org_user = OrganizationUser.objects.get(organization_id=organization, user_id=request.user)
        except:
            return False
        return request.method == 'GET' or org_user.role in ('создатель', 'ПМ')
