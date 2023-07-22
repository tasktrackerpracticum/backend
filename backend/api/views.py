from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.filters import TaskFilter, UserFilter, ProjectFilter
from api.permissions import (
    IsOrganizationCreator, IsAuthenticated, IsAdminUser, IsSelf,
    IsProjectManager, IsObserverTask, IsBaseUserTask, IsProjectManagerTask,
    IsProjectManagerComment, IsObserverComment, IsBaseUserComment
)
from api.serializers import (
    AddCommentSerializer, OrganizationViewSerializer,
    OrganizationCreateSerializer, ProjectSerializer,
    OrganizationUserAddSerializer, ProjectCreateSerializer,
    ProjectUserAddSerializer, TaskAddSerializer, TaskSerializer,
    TaskUserAddSerializer, CommentSerializer
)
from api.schemas import (
    user_id_param, pk_param, project_id_param, project_id_in_query,
    task_id_param, organization_id_param
    )
from tasks.models import (
    Organization, OrganizationUser, Project, ProjectUser, Task, Comment
)
from users.models import User


class UserViewSet(DjoserUserViewSet):
    permission_classes = (IsAuthenticated | IsAdminUser | IsSelf,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = UserFilter
    search_fields = ('email', 'username', 'phone', 'position', 'position',
                     'country', 'first_name', 'last_name')
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

    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'current_password': openapi.Schema(
                        type=openapi.TYPE_STRING)
                },
            ),
        )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OrganizationViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('title',)
    search_fields = ('title',)
    update_permision_classes = (IsOrganizationCreator,)
    serializer_class = OrganizationViewSerializer
    action_serializers = {
        'update': OrganizationUserAddSerializer,
    }

    def get_queryset(self):
        """Возвращает только те Организации, в которых участвует авторизованный
        пользователь, для администратора - все организации"""
        if self.request.user.is_authenticated:
            return Organization.objects.filter(users=self.request.user).all()
        return Organization.objects.all()

    def get_permissions(self):
        if self.action in ('patch', 'put', 'destroy', 'delete_user'):
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

    @swagger_auto_schema(manual_parameters=[pk_param])
    def retrieve(self, request, *args, **kwargs):
        """В этом эндпоинте можно посмотреть конкретную
        организацию и ее пользователей."""
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """В этом эндпоинте можно получить весь список
        организаций авторизованного пользователя."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[pk_param])
    @action(
        methods=['POST'],
        detail=True,
        serializer_class=OrganizationUserAddSerializer
    )
    def users(self, request, *args, **kwargs):
        """В этом эндпоинте можно добавить пользователя или изменить его роль в
        огранизации.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        organization = self.get_object()
        self.check_object_permissions(organization, request)
        user = User.objects.get(email=serializer.data.get('email'))
        obj, _ = OrganizationUser.objects.update_or_create(
            organization=organization,
            user=user,
            defaults={'role': serializer.data.get('role')}
        )
        obj.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(manual_parameters=[pk_param])
    def partial_update(self, request, *args, **kwargs):
        """В этом эндпоинте можно переименовать организацию."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[pk_param])
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """В этом эндпоинте можно удалить организацию."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[pk_param, user_id_param])
    @transaction.atomic
    def delete_user(self, request, *args, **kwargs):
        """В этом эндпоинте можно удалить пользователя из организации."""
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        organization = self.get_object()
        org_user = OrganizationUser.objects.get(
            user=user, organization=organization)
        org_user.delete()
        if not OrganizationUser.objects.filter(
            organization=organization
        ).exists():
            organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectViewSet(ModelViewSet):
    permission_classes = (IsProjectManager | IsAdminUser,)
    serializer_class = ProjectSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'project_id'
    queryset = Project.objects.all()
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter)
    filterset_class = ProjectFilter
    
    ordering_fields = ('title', 'is_active', 'date_start', 'date_finish')

    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[project_id_param])
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """В этом эндпоинте можно удалить проект."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[project_id_param])
    def retrieve(self, request, *args, **kwargs):
        """В этом энпоинте можно посмотреть конкретный проект."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[project_id_param])
    def partial_update(self, request, *args, **kwargs):
        """В этом эндпоинте можно переименовать проект."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[project_id_param, user_id_param])
    @transaction.atomic
    def delete_user(self, request, *args, **kwargs):
        """В этом эндпоинте можно удалить пользователя в проекте."""
        user_id = self.kwargs.get('user_id')
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

    @transaction.atomic
    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[organization_id_param])
    def create(self, request, *args, **kwargs):
        """В этом эндпоинте можно создать новый проект у организации."""
        serializer = ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            organization = Organization.objects.get(
                pk=kwargs.get('organization_id'))
        except ObjectDoesNotExist:
            raise NotFound('Организации с таким id не существует')
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
        response = serializer.data
        response.update({'id': project.pk})
        project_user.save()
        return Response(
            response, status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(manual_parameters=[project_id_param])
    @action(
        methods=['POST'],
        detail=True,
        serializer_class=ProjectUserAddSerializer,
    )
    def users(self, request, *args, **kwargs):
        """В этом эндпоинте можно добавить пользователя или изменить его роль в
        проекте.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        project = self.get_object()
        try:
            user = User.objects.get(email=serializer.data.get('email'))
        except ObjectDoesNotExist:
            raise NotFound('пользователя с таким id не существует')
        obj, _ = ProjectUser.objects.update_or_create(
            project=project,
            user=user,
            defaults={'role': serializer.data.get('role')}
        )
        obj.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )


class TasksViewSet(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (
        IsProjectManagerTask | IsObserverTask | IsBaseUserTask,
    )
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_class = TaskFilter
    search_fields = ('title',)
    ordering_fields = ('deadline', )
    ordering = ('deadline',)
    action_serializers = {
        'create': TaskAddSerializer,
        'partial_update': TaskAddSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(
                self.action, self.serializer_class)
        return super(OrganizationViewSet, self).get_serializer_class()

    @swagger_auto_schema(manual_parameters=[project_id_in_query])
    def list(self, request):
        """Отображает список задач конкретного проекта."""
        return super().list(request)

    @swagger_auto_schema(manual_parameters=[pk_param])
    def partial_update(self, request, **kwargs):
        """Позволяет изменить основные параметры задачи."""
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid()
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Создает задачу."""
        data = request.data
        data.update({'author': self.request.user})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(manual_parameters=[pk_param])
    @action(
        methods=['POST'],
        detail=True,
        serializer_class=TaskUserAddSerializer,
    )
    def users(self, request, **kwargs):
        """Добавляет пользователей в задачу."""
        try:
            task = Task.objects.get(pk=kwargs.get('pk'))
        except ObjectDoesNotExist:
            raise NotFound('задачи с таким id не существует')
        serializer = self.get_serializer(
            data={'email': request.data.get('email')})
        serializer.is_valid()
        try:
            user = User.objects.get(email=serializer.data.get('email'))
        except ObjectDoesNotExist:
            raise NotFound('пользователь с таким email не существует.')
        task.users.add(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if self.request.method == 'GET' and project_id:
            return Task.objects.filter(
                project_id=project_id,
            ).all()
        return super().get_queryset()

    @swagger_auto_schema(manual_parameters=[pk_param])
    def destroy(self, request, pk):
        """Удаляет задачу."""
        instance = self.get_object()
        instance.column = 'Удалено'
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(manual_parameters=[task_id_param, user_id_param])
    def user_delete(self, *args, **kwargs):
        """Удаляет пользователя из задачи."""
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise NotFound('Пользователя с таким id не существует.')
        task = self.get_object()
        task.users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = AddCommentSerializer
    permission_classes = (
        IsProjectManagerComment | IsObserverComment | IsBaseUserComment,
    )
    action_serializers = {
        'list': CommentSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(
                self.action, self.serializer_class)
        return super().get_serializer_class()

    def get_queryset(self):
        if not self.kwargs.get('task_id'):
            return super().get_queryset()
        try:
            return Task.objects.get(
                pk=self.kwargs.get('task_id')).comments.all()
        except ObjectDoesNotExist as e:
            raise NotFound(detail='Задачи с таким id не существует') from e

    @swagger_auto_schema(manual_parameters=[task_id_param])
    def list(self, request, *args, **kwargs):
        """Выдает все комментарии определенной задачи."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[task_id_param])
    def create(self, request, *args, **kwargs):
        """Создает новый комментарий к задаче."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = Task.objects.get(pk=kwargs.get('task_id'))
        comment = Comment.objects.create(
            author=request.user, task=task, **serializer.data)
        comment.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(tags=['tasks'])
    def destroy(self, request, *args, **kwargs):
        """Удаляет комментарий."""
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=['tasks'])
    def update(self, request, *args, **kwargs):
        """Изменяет комментарий."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['tasks'])
    def partial_update(self, request, *args, **kwargs):
        """Позволяет частично изменить комментарий."""
        return super().partial_update(request, *args, **kwargs)
