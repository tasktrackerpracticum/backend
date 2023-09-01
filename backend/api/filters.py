from django_filters import rest_framework as filters
from rest_framework import filters as f

from django.db.models import Case, IntegerField, Q, QuerySet, Value, When

from tasks.models import Project, Tag, User


class CustomProjectOrderingFilter(f.OrderingFilter):
    ordering_description = f'''Позволяет сортировать по полям модели Project: 
    {", ".join(
        [i.name for i in Project._meta.get_fields() if not i.is_relation])}'''


class TaskFilter(filters.FilterSet):
    search_doc = """
    Позволяет производить поиск по имени, фамилии, email пользователя,
    а также по названию задачи и ее описанию.
    """
    search = filters.CharFilter(method='custom_search', help_text=search_doc)

    def custom_search(self, queryset: QuerySet, _, value: str):
        users = User.objects.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )
        q1 = Q(title__istartswith=value)
        q2 = Q(title__icontains=value)
        q3 = Q(users__in=users)
        q4 = Q(author__in=users)
        q5 = Q(description__icontains=value)
        return queryset.filter(
            q1 | q2 | q3 | q4 | q5
        ).annotate(
            search_ordering=Case(
                When(q1, then=Value(1)),
                When(q2, then=Value(2)),
                When(q3, then=Value(3)),
                When(q4, then=Value(4)),
                When(q5, then=Value(5)),
                default=Value(100),
                output_field=IntegerField(),
            )
        ).order_by('search_ordering')


class UserFilter(filters.FilterSet):

    class Meta:
        model = User
        fields = '__all__'
        exclude = ('photo',)


class ProjectFilter(filters.FilterSet):
    search_doc = """Позволяет фильтровать по названию проекта,
    имени, фамилии пользователя и его email."""
    search = filters.CharFilter(method='custom_search', help_text=search_doc)
    tag = filters.CharFilter(
        method='tag_filter', help_text='Фильтрует проекты по названию тега')

    def custom_search(self, queryset: QuerySet, _, value: str):
        q1 = Q(title__istartswith=value)
        q2 = Q(title__icontains=value)
        users = User.objects.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )
        q3 = Q(users__in=users)
        return queryset.filter(
            q1 | q2 | q3
        ).annotate(
            search_ordering=Case(
                When(q1, then=Value(1)),
                When(q2, then=Value(2)),
                When(q3, then=Value(3)),
                default=Value(100),
                output_field=IntegerField(),
            )
        ).order_by('search_ordering')

    def tag_filter(self, queryset: QuerySet, _, value: str):
        project_ids = Tag.objects.filter(
            title__iexact=value).values_list('project')
        tag_projects = Project.objects.filter(pk__in=project_ids)
        return queryset & tag_projects

class TagFilter(filters.FilterSet):
    project = filters.NumberFilter(
        method='project_filter', help_text='Фильтрует теги по id проекта.')
    distinct = filters.CharFilter(
        method='distinct_filter',
        help_text='Выводит теги без повторений в названии. Варианты: true',
    )

    def project_filter(self, queryset: QuerySet, _, value):
        return queryset.filter(project_id=value)

    def distinct_filter(self, queryset: QuerySet, _, value):
        if value == 'true':
            return queryset.distinct('title')
        return queryset
