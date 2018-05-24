# Generated by Django 2.0.5 on 2018-05-22 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import project_dashboard.core.utils.time


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_auto_20180522_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, default=None, max_length=255, null=True, verbose_name='email')),
                ('token', models.CharField(blank=True, default=None, max_length=60, null=True, verbose_name='token')),
                ('invitation_extra_text', models.TextField(blank=True, null=True, verbose_name='invitation extra text')),
                ('user_order', models.BigIntegerField(default=project_dashboard.core.utils.time.timestamp_ms, verbose_name='user order')),
                ('invited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ihaveinvited+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='projects.Project')),
            ],
            options={
                'verbose_name': 'membership',
                'verbose_name_plural': 'memberships',
                'ordering': ['project', 'stakeholder__full_name', 'stakeholder__username', 'stakeholder__email', 'email'],
            },
        ),
        migrations.AlterField(
            model_name='stakeholder',
            name='user',
            field=models.OneToOneField(blank=True, help_text='(Optional) Link to User if available', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='stakeholder',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='membership',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='projects.Role'),
        ),
        migrations.AddField(
            model_name='membership',
            name='stakeholder',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='memberships', to='projects.Stakeholder'),
        ),
        migrations.RemoveField(
            model_name='role',
            name='project',
        ),
        migrations.RemoveField(
            model_name='stakeholder',
            name='project',
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('stakeholder', 'project')},
        ),
    ]
