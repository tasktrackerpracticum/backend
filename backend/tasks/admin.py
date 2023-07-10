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
    inlines = [
        OrganizationUserInline,
    ]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ProjectUserInline,
    ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    pass
