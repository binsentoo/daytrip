# Generated by Django 5.1 on 2024-09-17 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_manager', '0002_trip_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='id',
        ),
        migrations.AlterField(
            model_name='trip',
            name='UID',
            field=models.PositiveIntegerField(max_length=6, primary_key=True, serialize=False, unique=True),
        ),
    ]
