# Generated by Django 3.1.14 on 2022-03-22 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_userrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='parameters',
            field=models.JSONField(blank=True, max_length=500, null=True),
        ),
    ]