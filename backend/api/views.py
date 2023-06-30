from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permissions import IsCreatorOrReadOnly, IsProjectOrCreatorOrReadOnly
from .serializers import OrganizationViewSerializer, OrganizationCreateSerializer, ProjectSerializer
from tasks.models import Organization, OrganizationUser, Project
from users.models import User


class UserViewSet(UserViewSet):
    queryset = User.objects.all()


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
            organization_id=organization,
            user_id=request.user,
            role='создатель'
        )
        serializer = OrganizationViewSerializer(instance=organization)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request):
        organization = Organization.objects.filter(users=request.user).all()
        serializer = OrganizationViewSerializer(instance=organization, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsProjectOrCreatorOrReadOnly]
    serializer_class = ProjectSerializer
