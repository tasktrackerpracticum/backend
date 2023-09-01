from django.contrib import admin

from tasks.models import Comment, Project, ProjectUser, Tag, Task


class CommentInline(admin.TabularInline):
    model = Comment


class ProjectUserInline(admin.TabularInline):
    model = ProjectUser
    ordering = ('role', 'user')


class TagInline(admin.TabularInline):
    model = Tag


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'users__username')
    inlines = [
        ProjectUserInline, TagInline
    ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'status', 'deadline', 'project')
    list_filter = ('column', 'status')
    search_fields = (
        'title', 'description', 'users__username', 'author__username')
    inlines = [
        CommentInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'project')
