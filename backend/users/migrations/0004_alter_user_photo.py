# Generated by Django 4.2.2 on 2023-08-14 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='users', verbose_name='Фотография'),
        ),
    ]
