from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from .permissions import IsCreatorOrReadOnly, IsProjectOrCreatorOrReadOnly
from .serializers import (
    OrganizationViewSerializer, OrganizationCreateSerializer, ProjectSerializer,
    OrganizationUserAddSerializer
)
from tasks.models import Organization, OrganizationUser, Project
from users.models import User


class UserViewSet(DjoserUserViewSet):
    permission_classes = (IsAuthenticated,)
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
    


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    permission_classes = [IsCreatorOrReadOnly]
    serializer_class = OrganizationViewSerializer
    action_serializers = {
        'retrieve': OrganizationViewSerializer,
        'list': OrganizationViewSerializer,
        'create': OrganizationViewSerializer,
        'partial_update': OrganizationViewSerializer,
        'update': OrganizationUserAddSerializer,
        'delete': OrganizationViewSerializer,
    }

    def get_serializer_class(self):

        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(OrganizationViewSet, self).get_serializer_class()
 
    def create(self, request, *args, **kwargs):
        serializer = OrganizationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        organization = Organization.objects.get(title=request.data['title'])
        OrganizationUser.objects.create(
            organization=organization,
            user=request.user,
            role='создатель'
        )
        serializer = OrganizationViewSerializer(instance=organization)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request):
        organization = Organization.objects.filter(users=request.user).all()
        serializer = OrganizationViewSerializer(
            instance=organization, many=True
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers)
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = Organization.objects.get(id=kwargs.get('pk'))
        user = User.objects.get(id=serializer.initial_data.get('user'))
        org_user = OrganizationUser.objects.filter(
            organization=organization,
            user=user,
        )
        if org_user.exists():
            obj = OrganizationUser.objects.get(
                organization=organization,
                user=user,
            )
            obj.role = serializer.initial_data.get('role')
        else:
            obj =OrganizationUser.objects.create(
            organization=organization,
            user=user,
            role=serializer.initial_data.get('role'),
            )
        obj.save()
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )
            


class UserDeleteOrganizationViewSet(DestroyModelMixin, CreateModelMixin, GenericViewSet):
    queryset = OrganizationUser.objects.all()
    permission_classes = (IsCreatorOrReadOnly,)
    serializer_class = OrganizationUserAddSerializer
    lookup_field = 'organization__pk'
    lookup_url_kwarg = 'organization' 
     
    def get_object(self):
       qs = super().get_queryset()
       return qs.get(user__pk=self.kwargs.get('user_id'))
    
    # def create(self, request, *args, **kwargs):
    #     organization = Organization.objects.get(pk=kwargs.get('organization'))
    #     user = User.objects.get(pk=kwargs.get('user_id'))
    #     if OrganizationUser.objects.get(organization=organization, user=request.user).role == OrganizationUser.CREATOR:
    #         OrganizationUser.objects.create(organization=organization, user=user, role='')
        


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsProjectOrCreatorOrReadOnly]
    serializer_class = ProjectSerializer
