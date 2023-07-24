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

from api import filters as f
from api import permissions as p
from api import serializers as s
from api import schemas as schemas
from tasks.models import Project, ProjectUser, Task, Comment
from users.models import User


class UserViewSet(DjoserUserViewSet):
    permission_classes = (p.IsAuthenticated | p.IsAdminUser | p.IsSelf,)
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
        """
        В этом эндпоинте можно удалить пользователя.

        ---
        """
        return super().destroy(request, *args, **kwargs)


class ProjectViewSet(ModelViewSet):
    permission_classes = (p.IsProjectManager | p.IsAdminUser,)
    serializer_class = s.ProjectSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'project_id'
    queryset = Project.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = f.ProjectFilter
    ordering_fields = ('title', 'is_active', 'date_start', 'date_finish')
    action_serializers = {
        'list': s.ShortProjectSerializer,
    }

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def list(self, request, *args, **kwargs):
        """
        В этом эндпоинте можно посмотреть все проекты.

        ---
        """

    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[schemas.project_id_param])
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        В этом эндпоинте можно удалить проект.

        ---
        """
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[schemas.project_id_param])
    def retrieve(self, request, *args, **kwargs):
        """
        В этом энпоинте можно посмотреть конкретный проект.

        ---
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[schemas.project_id_param])
    def partial_update(self, request, *args, **kwargs):
        """
        В этом эндпоинте можно частично обновить проект.

        ---
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[schemas.project_id_param])
    def update(self, request, *args, **kwargs):
        """
        В этом эндпоинте можно обновить проект.

        ---
        """
        return super(ProjectViewSet, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[schemas.project_id_param])
    def create(self, request, *args, **kwargs):
        """
        В этом эндпоинте можно создать проект.

        ---
        """
        return super(ProjectViewSet, self).create(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[schemas.project_id_param])
    @action(
        methods=['POST'],
        detail=True,
        serializer_class=s.ProjectUserAddSerializer,
    )
    def users(self, request, *args, **kwargs):
        """
        В этом эндпоинте можно добавить пользователя или изменить его роль в
        проекте.

        ---
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        project = self.get_object()
        try:
            user = User.objects.get(email=serializer.data.get('email'))
        except ObjectDoesNotExist:
            raise NotFound('пользователя с таким email не существует')
        obj, _ = ProjectUser.objects.update_or_create(
            project=project,
            user=user,
            defaults={'role': serializer.data.get('role')}
        )
        obj.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[
            schemas.project_id_param, schemas.user_id_param])
    @transaction.atomic
    def delete_user(self, request, *args, **kwargs):
        """
        В этом эндпоинте можно удалить пользователя из проекта.

        ---
        """
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


class TasksViewSet(ModelViewSet):
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'
    permission_classes = (
        p.IsProjectManagerTask | p.IsObserverTask | p.IsBaseUserTask,
    )
    serializer_class = s.TaskSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = f.TaskFilter
    ordering_fields = ('deadline', )
    ordering = ('deadline',)
    action_serializers = {
        'create': s.TaskAddSerializer,
        'partial_update': s.TaskAddSerializer,
        'update': s.TaskAddSerializer,
    }

    def get_queryset(self):
        if project_id := self.kwargs.get('project_id'):
            try:
                project = Project.objects.get(pk=project_id)
            except ObjectDoesNotExist:
                raise NotFound('Проекта с таким id не существует')
        if self.request.method == 'GET' and project_id:
            return Task.objects.filter(
                project_id=project_id,
            ).all()
        return super().get_queryset()

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(
                self.action, self.serializer_class)
        return super().get_serializer_class()

    @swagger_auto_schema(
        manual_parameters=[schemas.project_id_param], tags=['tasks'])
    def list(self, *args, **kwargs):
        """
        Отображает список задач конкретного проекта.

        ---
        """
        return super().list(*args, **kwargs)

    @swagger_auto_schema(manual_parameters=[
        schemas.project_id_param, schemas.task_id_param], tags=['tasks'])
    def partial_update(self, request, *args, **kwargs):
        """
        Этот эндпоинт позволяет изменить основные параметры задачи.

        ---
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[
        schemas.project_id_param, schemas.task_id_param], tags=['tasks'])
    def update(self, request, *args, **kwargs):
        """
        В этом эндпоинте можно обновить параметры задачи.

        ---
        """
        partial = kwargs.pop('partial', False)
        task = self.get_object()
        serializer = self.get_serializer(
            task, data=request.data, partial=partial)
        serializer.is_valid()
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[schemas.project_id_param], tags=['tasks'])
    def create(self, request, *args, **kwargs):
        """
        Этот эндпоинт позволяет создать задачу.

        ---
        """
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(manual_parameters=[
        schemas.project_id_param, schemas.task_id_param], tags=['tasks'])
    @action(
        methods=['POST'],
        detail=True,
        serializer_class=s.TaskUserAddSerializer,
    )
    def users(self, request, **kwargs):
        """
        Этот эндпоинт добавляет пользователей в задачу.

        ---
        """
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

    @swagger_auto_schema(manual_parameters=[
        schemas.task_id_param, schemas.project_id_param], tags=['tasks'])
    def destroy(self, *args, **kwargs):
        """
        Этот эндпоинт удаляет задачу.

        ---
        """
        instance = self.get_object()
        instance.column = 'Удалено'
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(manual_parameters=[
        schemas.task_id_param, schemas.user_id_param], tags=['tasks'])
    def delete_user(self, *args, **kwargs):
        """
        Этот эндпоинт удаляет пользователя из задачи.

        ---
        """
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
    serializer_class = s.AddCommentSerializer
    permission_classes = (
        p.IsProjectManagerComment | p.IsObserverComment | p.IsBaseUserComment,
    )
    action_serializers = {
        'list': s.CommentSerializer,
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

    @swagger_auto_schema(
        manual_parameters=[schemas.task_id_param], tags=['comments'])
    def list(self, request, *args, **kwargs):
        """
        Этот эндпоинт отображает все комментарии задачи.

        ---
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[schemas.task_id_param], tags=['comments'])
    def create(self, request, *args, **kwargs):
        """
        Этот эндпоинт создает новый комментарий к задаче.

        ---
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = Task.objects.get(pk=kwargs.get('task_id'))
        comment = Comment.objects.create(
            author=request.user, task=task, **serializer.data)
        comment.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(tags=['comments'])
    def destroy(self, request, *args, **kwargs):
        """
        Этот эндпоинт удаляет комментарий.

        ---
        """
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=['comments'])
    def update(self, request, *args, **kwargs):
        """
        Этот эндпоинт изменяет комментарий.

        ---
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['comments'])
    def partial_update(self, request, *args, **kwargs):
        """
        Этот эндпоинт позволяет частично изменить комментарий.

        ---
        """
        return super().partial_update(request, *args, **kwargs)
