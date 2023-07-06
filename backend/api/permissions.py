from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.models import User
from tasks.models import Organization, OrganizationUser

class BaseRolePermission(IsAuthenticated):
    role = None

    def has_object_permission(self, request, view, obj):
        if obj.users.filter(id=request.user.id).exists():
            role = OrganizationUser.objects.get(
                user=request.user, organization=obj).role
            if role==OrganizationUser.FORBIDDEN:
                return False
            return role==self.role
        return False
    

class IsCreator(BaseRolePermission):
    role = OrganizationUser.CREATOR


class IsProjectManager(BaseRolePermission):
    role = OrganizationUser.PROJECT_MANAGER

    
class IsObserver(BaseRolePermission):
    role = OrganizationUser.OBSERVER

    
class IsBaseUser(BaseRolePermission):
    role = OrganizationUser.BASE_USER
    

class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        ids = []
        for user in obj.users.all():
            org_user = OrganizationUser.objects.get(organization=obj, user=user)
            if org_user.role == 'создатель':
                ids.append(user.id)
        return request.user.id in ids


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
