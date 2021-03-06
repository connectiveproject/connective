# Generated by Django 3.1.11 on 2021-12-23 15:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_event_cancellation_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ext_consumers_attended',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='event',
            name='summary_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
