from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from tasks.models import Comment, Project, ProjectUser, Task, Tag
from users.models import User


class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'chat_id', 'phone',
            'photo', 'last_login', 'chat_id'
        )


class ProjectUserAddSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=ProjectUser.ROLES)

    class Meta:
        fields = ('email', 'role')


class UserCommentSerializer(serializers.ModelSerializer):
    photo = Base64ImageField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'photo')


class UserSerializer(serializers.ModelSerializer):
    photo = Base64ImageField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'photo',
            'phone', 'position', 'date_of_birth', 'gender',
            'country', 'timezone', 'last_login', 'chat_id', 'notify_in_chat'
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

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'title', 'project')
        read_only_fields = ('project',)

    def validate(self, attrs):
        project = self.context['view'].kwargs.get('project_id')
        user = self.context['request'].user
        tag = Tag.objects.filter(
            title=attrs.get('title'), user=user, project=project)
        if tag.exists():
            raise ValidationError(detail='Такой тег уже существует')
        return attrs



class ShortProjectSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id', 'title', 'description', 'date_start', 'date_finish',
            'is_active', 'users', 'created_at', 'updated_at', 'tags'
        )

    def get_users(self, obj):
        users = ProjectUser.objects.filter(project=obj)
        serializer = ProjectUserSerializer(
            users, many=True, context=self.context)
        return serializer.data

    def get_tags(self, obj):
        tags = Tag.objects.filter(
            project=obj, user=self.context['request'].user)
        return TagSerializer(tags, many=True).data


class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    tasks = TaskSerializer(many=True, read_only=True)
    tags = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = (
            'id', 'title', 'description', 'date_start', 'date_finish',
            'is_active', 'users', 'tasks', 'created_at', 'updated_at', 'tags'
    )

    def get_users(self, obj):
        users = ProjectUser.objects.filter(project=obj)
        return ProjectUserSerializer(users, many=True, context=self.context).data

    def get_tags(self, obj):
        tags = Tag.objects.filter(
            project=obj, user=self.context['request'].user)
        return TagSerializer(tags, many=True, context=self.context).data

class ProjectCreateSerializer(serializers.ModelSerializer):
    users = ProjectUserAddSerializer(many=True)

    class Meta:
        model = Project
        fields = (
            'title', 'description', 'date_start', 'date_finish',
            'users'
        )
    @transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
        users = validated_data.pop('users')
        project = Project.objects.create(**validated_data)
        user_project = ProjectUser.objects.create(
            user=author,
            project=project,
            role=ProjectUser.PROJECT_MANAGER
        )
        user_project.save()
        for user in users:
            try:
                user_instance = User.objects.get(email=user.get('email'))
                ProjectUser.objects.create(
                    user=user_instance,
                    project=project,
                    role=user.get('role')
                )
            except ObjectDoesNotExist:
                pass
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
