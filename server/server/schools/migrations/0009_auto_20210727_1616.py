# Generated by Django 3.1.11 on 2021-07-27 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0008_importedschool'),
    ]

    operations = [
        migrations.RenameField(
            model_name='school',
            old_name='zip_city',
            new_name='address_zipcode',
        ),
    ]
