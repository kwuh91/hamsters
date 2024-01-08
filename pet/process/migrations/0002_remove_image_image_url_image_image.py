# Generated by Django 4.2.7 on 2024-01-08 05:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image_url',
        ),
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='images/'),
            preserve_default=False,
        ),
    ]
