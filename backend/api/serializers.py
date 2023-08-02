from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import NotFound
from tasks.models import Comment, Project, ProjectUser, Task
from users.models import User


class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'chat_id', 'phone',
            'photo', 'last_login',
        )


class ProjectUserAddSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = ProjectUser
        fields = ('email', 'role')


class UserCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'photo')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'photo',
            'phone', 'position', 'date_of_birth', 'gender',
            'country', 'timezone', 'last_login',
        )


class ProjectUserSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()

    class Meta:
        model = ProjectUser
        fields = ('user', 'role')


class CommentSerializer(serializers.ModelSerializer):
    author = UserCommentSerializer()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ('text', 'author', 'created_at', 'updated_at')


class AddCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text',)


class TaskSerializer(serializers.ModelSerializer):
    users = ShortUserSerializer(many=True, read_only=True)
    author = ShortUserSerializer()


class TaskSerializer(serializers.ModelSerializer):
    users = ShortUserSerializer(many=True, read_only=True)
    author = ShortUserSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'column', 'users', 'author',
            'status', 'deadline', 'comments', 'created_at', 'updated_at',
            'ordering'
        )


class ShortProjectSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'title', 'description', 'date_start', 'date_finish',
            'is_active', 'users', 'created_at', 'updated_at',
        )

    def get_users(self, obj):
        users = ProjectUser.objects.filter(project=obj)
        return ProjectUserSerializer(users, many=True).data


class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    tasks = TaskSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'title', 'description', 'date_start', 'date_finish',
            'is_active', 'users', 'tasks', 'created_at', 'updated_at',
    )

    def get_users(self, obj):
        users = ProjectUser.objects.filter(project=obj)
        return ProjectUserSerializer(users, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
        project = Project.objects.create(**validated_data)
        user_project = ProjectUser.objects.create(
            user=author,
            project=project,
            role=ProjectUser.PROJECT_MANAGER
        )
        user_project.save()
        return project

######!!!!
class TaskAddSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = (
            'title', 'description', 'column', 'status', 'deadline', 'author',
        )

    def create(self, validated_data):
        try:
            project = Project.objects.get(
                pk=self.context['view'].kwargs.get('project_id'))
        except ObjectDoesNotExist:
            raise NotFound('Проекта с таким id не существует')
        instance = Task.objects.create(**validated_data, project=project)
        return instance


class TaskEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'title', 'description', 'column', 'status', 'deadline',
        )


class TaskUserAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)
