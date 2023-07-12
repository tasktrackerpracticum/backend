from django_filters import rest_framework as filters

from tasks.models import Task


class TaskFilter(filters.FilterSet):
    project_id = filters.CharFilter()

    class Meta:
        model = Task
        fields = ('project_id',)
