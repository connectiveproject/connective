# Generated by Django 3.1.11 on 2021-07-27 14:03

from django.db import migrations, models
import server.utils.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20210718_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='events_sequence_slug',
            field=models.CharField(default=server.utils.model_fields.random_slug, max_length=40),
        ),
    ]
