# Generated by Django 3.2.12 on 2022-04-10 09:35

from django.db import migrations, models
import django.db.models.deletion
import server.utils.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20220405_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default=server.utils.model_fields.random_slug, max_length=40, unique=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Event Series',
                'verbose_name_plural': 'Event Series',
            },
        ),
        migrations.AlterField(
            model_name='eventorder',
            name='recurrence',
            field=models.CharField(choices=[('ONE_TIME', 'One Time'), ('WEEKLY', 'Weekly'), ('WEEKLY_NUMBERED', 'Weekly (numbered)')], default='ONE_TIME', max_length=50, verbose_name='recurrence'),
        ),
        migrations.AddField(
            model_name='event',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='events.eventseries'),
        ),
    ]
