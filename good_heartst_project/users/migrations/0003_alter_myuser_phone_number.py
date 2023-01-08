# Generated by Django 3.2.15 on 2023-01-07 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_myuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='phone_number',
            field=models.CharField(default='+7 999 999 99 99', max_length=20, unique=True, verbose_name='Номер телефона пользователя'),
        ),
    ]