from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import DestroyModelMixin
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


class UserDeleteOrganizationViewSet(DestroyModelMixin, GenericViewSet):
    queryset = OrganizationUser.objects.all()
    permission_classes = (IsCreatorOrReadOnly,)
    serializer_class = OrganizationUserAddSerializer
    lookup_field = 'organization__pk'
    lookup_url_kwarg = 'organization' 
     
    def get_object(self):
       qs = super().get_queryset()
       return qs.get(user__pk=self.kwargs.get('user_id'))


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsProjectOrCreatorOrReadOnly]
    serializer_class = ProjectSerializer
