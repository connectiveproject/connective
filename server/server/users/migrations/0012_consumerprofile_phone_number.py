# Generated by Django 3.1.11 on 2021-10-26 07:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20211006_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message='phone number must be between 9-15 digits', regex='^\\d{9,15}$')]),
        ),
    ]
