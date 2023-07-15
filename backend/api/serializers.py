from rest_framework import serializers

from tasks.models import (Comment, Organization, OrganizationUser, Project,
                          ProjectUser, Task)
from users.models import User


class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'phone', 'photo')


class CommentSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer()

    class Meta:
        model = Comment
        fields = ('task', 'description', 'image', 'author')


class AddCommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.ImageField()

    class Meta:
        model = Comment
        fields = ('description', 'image', 'author')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'photo',
            'phone', 'position', 'date_of_birth', 'gender',
            'country', 'timezone',
        )


class OrganizationUserSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()

    class Meta:
        model = OrganizationUser
        fields = ('role', 'user')


class OrganizationUserAddSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=OrganizationUser.ROLES)

    class Meta:
        model = User
        fields = ('email', 'role')


class OrganizationUserDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)


class ProjectUserAddSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ProjectUser.ROLES)

    class Meta:
        model = User
        fields = ('email', 'role')


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


class ProjectUserSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()

    class Meta:
        model = ProjectUser
        fields = ('user', 'role')


class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'title', 'users')

    def get_users(self, obj):
        users = ProjectUser.objects.filter(project=obj)
        return ProjectUserSerializer(users, many=True).data


class ProjectCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title')


class TaskSerializer(serializers.ModelSerializer):
    users = ShortUserSerializer(many=True)
    author = ShortUserSerializer()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'title', 'description', 'column', 'users', 'author',
            'status', 'deadline', 'comments'
        )

    def get_comments(self, obj):
        return CommentSerializer(obj.comments, many=True).data


class TaskAddSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = (
            'title', 'description', 'column', 'status', 'deadline', 'author',
            'project'
        )


class TaskEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'title', 'description', 'column', 'status', 'deadline',
            'project'
        )


class TaskUserAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)
