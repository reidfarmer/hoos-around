# Generated by Django 4.2.6 on 2023-11-02 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_event_latitude_event_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
