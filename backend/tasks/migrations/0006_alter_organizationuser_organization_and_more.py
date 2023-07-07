# Generated by Django 4.2.2 on 2023-07-05 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0005_rename_task_id_comment_task_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationuser',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_users', to='tasks.organization'),
        ),
        migrations.AlterField(
            model_name='organizationuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_organizations', to=settings.AUTH_USER_MODEL),
        ),
    ]