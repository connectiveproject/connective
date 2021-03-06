# Generated by Django 3.1.11 on 2021-10-06 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_user_terms_of_use_acceptance_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerprofile',
            name='invitation_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='consumerprofile',
            name='last_invite_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coordinatorprofile',
            name='invitation_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coordinatorprofile',
            name='last_invite_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='instructorprofile',
            name='invitation_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='instructorprofile',
            name='last_invite_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='supervisorprofile',
            name='invitation_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='supervisorprofile',
            name='last_invite_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vendorprofile',
            name='invitation_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vendorprofile',
            name='last_invite_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
