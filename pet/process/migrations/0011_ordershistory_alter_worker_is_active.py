# Generated by Django 4.2.7 on 2024-01-13 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0010_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_login', models.CharField(max_length=255, unique=True)),
                ('client_name', models.CharField(max_length=255)),
                ('client_email', models.EmailField(max_length=254)),
                ('client_phone_number', models.CharField(max_length=11)),
                ('salon_address', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='worker',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]