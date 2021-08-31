# Generated by Django 3.1.11 on 2021-08-31 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0026_auto_20210812_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolactivityorder',
            name='status_reason',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='schoolactivityorder',
            name='status',
            field=models.CharField(choices=[('CANCELLED', 'Cancelled'), ('PENDING_ADMIN_APPROVAL', 'Pending Admin Approval'), ('APPROVED', 'Approved'), ('DENIED', 'Denied')], default='PENDING_ADMIN_APPROVAL', max_length=50, verbose_name='status'),
        ),
    ]