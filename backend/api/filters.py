from django_filters import rest_framework as filters

from tasks.models import Task, User, Project


class TaskFilter(filters.FilterSet):
    project_id = filters.CharFilter()

    class Meta:
        model = Task
        fields = ('project_id',)


class UserFilter(filters.FilterSet):

    class Meta:
        model = User
        fields = '__all__'
        exclude = ('photo',)


class ProjectFilter(filters.FilterSet):

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('deadline',)
