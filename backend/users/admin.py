from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin settings for user model."""

    model = User
    fields = (
        'email', 'username', 'first_name', 'last_name', 'chat_id', 'phone',
        'position', 'gender', 'is_staff', 'is_active', 'photo', 'country',
        'timezone',
    )
    search_fields = ('first_name', 'username', 'email', 'phone')
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'chat_id', 'phone',
        'country',
    )
    list_filter = ('country', 'is_active', 'is_staff')
    ordering = ('is_active', 'date_joined', 'username', 'email')
