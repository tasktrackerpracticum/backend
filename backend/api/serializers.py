from rest_framework import serializers

from tasks.models import Organization, OrganizationUser, Project
from users.models import User


class OrganizationUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationUser
        fields = ('id', 'role', 'user')
    
    def get_user(self, obj):
        return obj.user.email
    
    def get_id(self, obj):
        return obj.user.pk


class OrganizationUserAddSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    role = serializers.ChoiceField(choices=OrganizationUser.ROLES)
    delete_user = serializers.BooleanField()

    class Meta:
        model = OrganizationUser
        fields = ('user', 'role', 'organization', 'delete_user')
        
    def get_organization(self, _):
        return Organization.objects.get(
            pk=self.context.get('view').kwargs.get('pk')).pk
        

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


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'photo',
            'phone', 'position', 'date_of_birth', 'gender',
            'country', 'timezone',
        )
