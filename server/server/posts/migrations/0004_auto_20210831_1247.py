# Generated by Django 3.1.11 on 2021-08-31 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20210727_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=models.TextField(max_length=300),
        ),
    ]
