# Generated by Django 3.1.11 on 2021-06-10 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_auto_20210608_1047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolactivitygroup',
            name='container_only',
        ),
        migrations.AddField(
            model_name='schoolactivitygroup',
            name='group_type',
            field=models.CharField(choices=[('CONTAINER_ONLY', 'Container Only'), ('DISABLED_CONSUMERS', 'Disabled Consumers'), ('DEFAULT', 'Default')], default='DEFAULT', max_length=50, verbose_name='group type'),
        ),
    ]
