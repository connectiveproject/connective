# Generated by Django 3.1.11 on 2022-01-06 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import server.utils.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_consumerprofile_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default=server.utils.model_fields.random_slug, max_length=40, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notification_code', models.CharField(max_length=100)),
                ('parameters', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('READ', 'Read'), ('DISMISSED', 'Dismissed')], default='NEW', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]