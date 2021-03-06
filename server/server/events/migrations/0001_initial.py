# Generated by Django 3.1.11 on 2021-06-08 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_auto_20210608_1047'),
        ('organizations', '0004_auto_20210608_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('locations_name', models.CharField(blank=True, max_length=250, null=True)),
                ('consumers', models.ManyToManyField(to='users.Consumer')),
                ('school_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizations.schoolactivitygroup')),
            ],
        ),
    ]
