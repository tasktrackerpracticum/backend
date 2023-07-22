from django.db.models import QuerySet, Q, Case, IntegerField, Value, When
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
    search = filters.CharFilter(method='custom_search')

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('deadline',)

    def custom_search(self, queryset: QuerySet, _, value: str):
        q1 = Q(title__istartswith=value)
        user = User.objects.filter(Q(first_name__istartswith=value)
                                   | Q(last_name__istartswith=value))
        q2 = Q(users__in=user)
        return queryset.filter(
            q1 | q2
        )
