from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, UpdateModelMixin, DestroyModelMixin,
    RetrieveModelMixin
)
from drf_yasg.utils import swagger_auto_schema

from api.filters import TaskFilter
from api.permissions import (
    IsOrganizationCreator, IsAuthenticated, IsAdminUser, IsSelf,
    IsProjectManager, IsObserverTask, IsBaseUserTask, IsProjectManagerTask,
    IsProjectManagerComment, IsObserverComment, IsBaseUserComment
)
from api.serializers import (
    OrganizationViewSerializer, OrganizationCreateSerializer,
    ProjectSerializer, OrganizationUserAddSerializer, ProjectCreateSerializer,
    ProjectUserAddSerializer, TaskSerializer, TaskUserAddSerializer,
    CommentSerializer
)
from api.schemas import (
    user_id_param, pk_param, project_id_param,
    )
from tasks.models import (
    Organization, OrganizationUser, Project, ProjectUser, Task, Comment
)
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

    @swagger_auto_schema(manual_parameters=[pk_param])
    def retrieve(self, request, *args, **kwargs):
        """В этом эндпоинте можно посмотреть конкретную
        организацию и ее пользователей."""
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """В этом эндпоинте можно получить весь список
        организаций авторизованного пользователя."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[pk_param, user_id_param])
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

    @swagger_auto_schema(manual_parameters=[pk_param])
    def partial_update(self, request, *args, **kwargs):
        """В этом эндпоинте можно переименовать организацию."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[pk_param])
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """В этом эндпоинте можно удалить организацию."""
        return super().destroy(request, *args, **kwargs)


class OrganizationDeleteUserViewSet(OrganizationViewSet):
    @swagger_auto_schema(manual_parameters=[pk_param, user_id_param])
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """В этом эндпоинте можно удалить пользователя из организации."""
        user_id = self.kwargs.get('user_id')
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


class SimpleProjectViewSet(
    UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin,
    BaseProjectViewset):

    @swagger_auto_schema(
        tags=["projects"], manual_parameters=[project_id_param, user_id_param])
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


class ProjectCreateViewSet(CreateModelMixin, BaseProjectViewset):

    @transaction.atomic
    @swagger_auto_schema(tags=["projects"])
    def create(self, request, *args, **kwargs):
        """В этом эндпоинте можно создать новый проект."""
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

    @swagger_auto_schema(manual_parameters=[project_id_param, user_id_param])
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


class TasksViewSet(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (
        IsProjectManagerTask | IsObserverTask | IsBaseUserTask,
    )
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def list(self, request):
        return super().list(request)

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if self.request.method == 'GET' and project_id:
            return Task.objects.filter(
                project_id=project_id,
            ).all()
        return super().get_queryset()

    def destroy(self, request, pk):
        instance = self.get_object()
        instance.column = 'Удалено'
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsProjectManagerTask],
        serializer_class=TaskUserAddSerializer,
    )
    def users(self, request, pk):
        try:
            task = Task.objects.get(id=pk)
        except Exception:
            return Response(
                status=status.HTTP_404_NOT_FOUND, data='Task not found'
            )
        try:
            user = User.objects.get(email=request.data.get('email'))
        except Exception:
            return Response(
                status=status.HTTP_404_NOT_FOUND, data='User not found'
            )
        if request.method == 'POST':
            if user in task.users.all():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data='User have already added in task'
                )
            task.users.add(user)
            return Response(status=status.HTTP_200_OK)
        if user not in task.users.all():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data='Can not delete user from task'
            )
        task.users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT, data='Deleted')


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsProjectManagerComment | IsObserverComment | IsBaseUserComment,
    )

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        task_id = self.request.query_params.get('task_id')
        if not project_id and not task_id:
            # return Response(status=status.HTTP_404_NOT_FOUND,
            # data='Project or task not found')
            # tasks = Task.objects.filter(project=project_id).filter(
            # id=task_id)
            return Comment.objects.none()
        tasks = Task.objects.filter(project_id=project_id, id=task_id)
        if not tasks.exists():
            return Comment.objects.none()
            # return Response(
            #     status=status.HTTP_404_NOT_FOUND,
            #     data='Something wrong with your query params'
            # )
        return Comment.objects.filter(
                task__in=tasks
            ).all()
