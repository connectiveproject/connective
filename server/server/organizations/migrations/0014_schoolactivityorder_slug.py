# Generated by Django 3.1.11 on 2021-06-29 09:12

from django.db import migrations, models
import server.utils.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0013_auto_20210624_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolactivityorder',
            name='slug',
            field=models.CharField(default=server.utils.model_fields.random_slug, max_length=40, null=True),
        ),
    ]
