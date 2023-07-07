from django.db import transaction
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from djoser.serializers import UserDeleteSerializer
from drf_yasg.utils import swagger_auto_schema

from .permissions import (
    IsOrganizationCreator, IsAuthenticated, IsAdminUser, IsSelf,
    IsProjectManager
)
from .serializers import (
    OrganizationViewSerializer, OrganizationCreateSerializer,
    ProjectSerializer, OrganizationUserAddSerializer, ProjectCreateSerializer,
    ProjectUserAddSerializer
)
from tasks.models import Organization, OrganizationUser, Project, ProjectUser
from users.models import User


class UserViewSet(DjoserUserViewSet):
    permission_classes = (IsAuthenticated | IsAdminUser | IsSelf,)
    queryset = User.objects.all()

    @action(["get", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    @swagger_auto_schema(request_body=UserDeleteSerializer)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OrganizationViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    update_permision_classes = (IsOrganizationCreator,)
    serializer_class = OrganizationViewSerializer
    action_serializers = {
        'update': OrganizationUserAddSerializer,
    }

    def get_queryset(self):
        """Возвращает только те Организации, в которых участвует авторизованный
        пользователь, для администратора - все организации"""
        if self.request.user.is_admin and self.request.user.is_active:
            return Organization.objects.all()
        return Organization.objects.filter(users=self.request.user).all()

    def get_permissions(self):
        if self.action in ('patch', 'put', 'destroy'):
            permission_classes = self.update_permision_classes
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(
                self.action, self.serializer_class)
        return super(OrganizationViewSet, self).get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """В этом эндпоинте создается организация, статус владельца
        автоматически получает авторизованный пользователь."""
        serializer = OrganizationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        organization = Organization.objects.get(title=request.data['title'])
        OrganizationUser.objects.create(
            organization=organization,
            user=request.user,
            role=OrganizationUser.CREATOR,
        )
        serializer = OrganizationViewSerializer(instance=organization)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        """В этом эндпоинте можно посмотреть конкретную
        организацию и ее пользователей."""
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """В этом эндпоинте можно получить весь список
        организаций авторизованного пользователя."""
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """В этом эндпоинте можно добавить пользователя или изменить его роль в
        огранизации.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = self.get_object()
        user = User.objects.get(id=serializer.data.get('user'))
        obj, _ = OrganizationUser.objects.update_or_create(
            organization=organization,
            user=user,
            defaults={'role': serializer.data.get('role')}
        )
        obj.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        """В этом эндпоинте можно переименовать организацию."""
        return super().partial_update(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """В этом эндпоинте можно удалить организацию
        или пользователя в организации."""
        user_id = self.kwargs.get('user_id')
        if not user_id:
            return super().destroy(request, *args, **kwargs)
        user = User.objects.get(id=user_id)
        organization = Organization.objects.get(id=self.kwargs.get('pk'))
        org_user = OrganizationUser.objects.get(
            user=user, organization=organization)
        org_user.delete()
        if not OrganizationUser.objects.filter(
            organization=organization
        ).exists():
            organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseProjectViewset(GenericViewSet):
    permission_classes = (IsProjectManager | IsAdminUser,)
    serializer_class = ProjectSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'project_id'
    queryset = Project.objects.all()


class ProjectViewSet(CreateModelMixin, ListModelMixin, BaseProjectViewset):

    def get_queryset(self):
        if self.request.user.is_admin and self.request.user.is_active:
            return Project.objects.filter(organization=self.kwargs.get('id'))
        return Project.objects.filter(users=self.request.user).all()

    @swagger_auto_schema(tags=["projects"])
    def list(self, request, *args, **kwargs):
        """В этом эндпоинте можно получить весь список
        проектов пользователя."""
        return super().list(request, *args, **kwargs)


class SimpleProjectViewSet(
    UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin,
    BaseProjectViewset
):

    @swagger_auto_schema(tags=["projects"])
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """В этом эндпоинте можно удалить проект
        или пользователя в проекте."""
        user_id = self.kwargs.get('user_id')
        if not user_id:
            return super().destroy(request, *args, **kwargs)
        user = User.objects.get(id=user_id)
        project = self.get_object()
        project_user = ProjectUser.objects.get(
            user=user, project=project)
        project_user.delete()
        if not ProjectUser.objects.filter(
            project=project,
        ).exists():
            project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(tags=["projects"])
    def retrieve(self, request, *args, **kwargs):
        """В этом энпоинте можно посмотреть конкретный проект."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["projects"])
    def partial_update(self, request, *args, **kwargs):
        """В этом эндпоинте можно переименовать проект."""
        return super().partial_update(request, *args, **kwargs)


class ProjectCreateViewSet(CreateModelMixin, BaseProjectViewset):

    @transaction.atomic
    @swagger_auto_schema(tags=["projects"])
    def create(self, request, *args, **kwargs):
        serializer = ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = Organization.objects.get(
            pk=kwargs.get('organization_id'))
        project = Project.objects.create(
            organization=organization,
            title=serializer.data.get('title'),
        )
        project.save()
        project_user = ProjectUser.objects.create(
            project=project,
            user=self.request.user,
            role=ProjectUser.PROJECT_MANAGER,
        )
        project_user.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED,
        )


class AddUserToProjectViewSet(UpdateModelMixin, BaseProjectViewset):
    serializer_class = ProjectUserAddSerializer

    def update(self, request, *args, **kwargs):
        """В этом эндпоинте можно добавить пользователя или изменить его роль в
        проекте.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = self.get_object()
        user = User.objects.get(id=serializer.data.get('user'))
        obj, _ = ProjectUser.objects.update_or_create(
            project=project,
            user=user,
            defaults={'role': serializer.data.get('role')}
        )
        obj.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )
