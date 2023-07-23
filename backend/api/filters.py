from django.db.models import QuerySet, Q, Case, IntegerField, Value, When
from django_filters import rest_framework as filters

from tasks.models import Task, User, Project


class TaskFilter(filters.FilterSet):
    project_id = filters.CharFilter()
    search = filters.CharFilter(method='custom_search')

    class Meta:
        model = Task
        fields = ('project_id', 'column', 'status',)

    def custom_search(self, queryset: QuerySet, _, value: str):
        q1 = Q(title__istartswith=value)
        users = User.objects.filter(Q(first_name__istartswith=value)
                                    | Q(last_name__istartswith=value))
        q2 = Q(users__in=users)
        q3 = Q(column__istartswith=value)
        q4 = Q(author__in=users)
        q5 = Q(description__istartswith=value)
        return queryset.filter(
            q1 | q2 | q3 | q4 | q5
        )


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
        users = User.objects.filter(Q(first_name__istartswith=value)
                                   | Q(last_name__istartswith=value))
        q2 = Q(users__in=users)
        return queryset.filter(
            q1 | q2
        )
