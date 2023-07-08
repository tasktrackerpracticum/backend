from rest_framework import serializers

from tasks.models import (
    Organization, OrganizationUser, Project, ProjectUser, Task
)
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'photo',
            'phone', 'position', 'date_of_birth', 'gender',
            'country', 'timezone',
        )


class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'position', 'phone')


class OrganizationUserSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()

    class Meta:
        model = OrganizationUser
        fields = ('role', 'user')


class OrganizationUserAddSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    role = serializers.ChoiceField(choices=OrganizationUser.ROLES)
    user = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationUser
        fields = ('user', 'role', 'organization')

    def get_organization(self, _):
        return Organization.objects.get(
            pk=self.context['view'].kwargs.get('pk')).pk

    def get_user(self, _):
        return User.objects.get(
            pk=self.context['view'].kwargs.get('user_id')).pk


class ProjectUserAddSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    role = serializers.ChoiceField(choices=ProjectUser.ROLES)
    user = serializers.SerializerMethodField()

    class Meta:
        model = ProjectUser
        fields = ('user', 'role', 'project')

    def get_project(self, _):
        return Project.objects.get(
            pk=self.context['view'].kwargs.get('project_id')).pk

    def get_user(self, _):
        return User.objects.get(
            pk=self.context['view'].kwargs.get('user_id')).pk


class OrganizationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('title',)


class OrganizationViewSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ('id', 'title', 'users')

    def get_users(self, obj):
        users = OrganizationUser.objects.filter(organization=obj)
        return OrganizationUserSerializer(users, many=True).data


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title')


class ProjectCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('title',)


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'title', 'description', 'column', 'users', 'project', 'author',
            'status', 'deadline'
        )


class TaskUserAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)
