# Generated by Django 4.2.2 on 2023-09-05 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_country_alter_user_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Должность'),
        ),
    ]