# Generated by Django 4.2.7 on 2024-01-09 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0008_worker_groups_worker_is_superuser_worker_last_login_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
