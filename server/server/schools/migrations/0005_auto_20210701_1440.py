# Generated by Django 3.1.11 on 2021-07-01 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schools', '0004_school_last_updated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_updated_by_me_schools', to=settings.AUTH_USER_MODEL),
        ),
    ]
