# Generated by Django 3.1.11 on 2021-07-25 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0022_importedactivity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='importedactivity',
            old_name='proffesion',
            new_name='profession',
        ),
        migrations.RemoveField(
            model_name='importedactivity',
            name='domain',
        ),
        migrations.RemoveField(
            model_name='importedactivity',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='importedactivity',
            name='originization',
        ),
        migrations.RemoveField(
            model_name='importedactivity',
            name='tags',
        ),
    ]
