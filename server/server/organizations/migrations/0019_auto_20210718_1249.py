# Generated by Django 3.1.11 on 2021-07-18 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0018_activity_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='domain',
            field=models.CharField(blank=True, choices=[('SCIENCE_AND_TECH', 'Science And Tech'), ('EXTREME_SPORTS', 'Extreme Sports'), ('FIELD', 'Field')], max_length=55, null=True),
        ),
    ]
