from django.contrib import admin

from tasks.models import (
    Comment, Organization, OrganizationUser, Project, ProjectUser, Subtask,
    Task
)


class CommentInline(admin.TabularInline):
    model = Comment


class OrganizationUserInline(admin.TabularInline):
    model = OrganizationUser
    ordering = ('role', 'user')


class ProjectUserInline(admin.TabularInline):
    model = ProjectUser
    ordering = ('role', 'user')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ('title', 'users__username')
    inlines = [
        OrganizationUserInline,
    ]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization')
    list_filter = ('organization',)
    search_fields = ('title', 'users__username', 'organization__title')
    inlines = [
        ProjectUserInline,
    ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'status', 'deadline')
    list_filter = ('column', 'status')
    search_fields = (
        'title', 'description', 'users__username', 'author__username')
    inlines = [
        CommentInline,
    ]


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    pass
