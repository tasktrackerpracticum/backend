from rest_framework import serializers

from tasks.models import Organization, OrganizationUser, Project
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
        fields = '__all__'