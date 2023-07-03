# Generated by Django 4.2.2 on 2023-07-03 05:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0003_alter_organizationuser_role'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='organizationuser',
            unique_together={('organization_id', 'user_id')},
        ),
    ]
