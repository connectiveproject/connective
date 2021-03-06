# Generated by Django 3.1.11 on 2021-06-08 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210608_1047'),
        ('schools', '0003_auto_20210530_1028'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0003_auto_20210526_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationmember',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_member', to='organizations.organization'),
        ),
        migrations.CreateModel(
            name='SchoolActivityOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CANCELLED', 'Cancelled'), ('PENDING_ADMIN_APPROVAL', 'Pending Admin Approval'), ('APPROVED', 'Approved')], default='PENDING_ADMIN_APPROVAL', max_length=50, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_activity_orders', to='organizations.activity')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_updated_by_me_orders', to=settings.AUTH_USER_MODEL)),
                ('requested_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requested_orders', to=settings.AUTH_USER_MODEL)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_activity_orders', to='schools.school')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolActivityGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('container_only', models.BooleanField(default=False)),
                ('activity_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_groups', to='organizations.schoolactivityorder')),
                ('consumers', models.ManyToManyField(related_name='activity_groups', to='users.Consumer')),
            ],
        ),
        migrations.AddConstraint(
            model_name='schoolactivityorder',
            constraint=models.UniqueConstraint(fields=('school', 'activity'), name='unique_order'),
        ),
    ]
