# Generated by Django 2.0.5 on 2018-05-18 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(related_name='projects', through='projects.Membership', to=settings.AUTH_USER_MODEL, verbose_name='members'),
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_projects', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AddField(
            model_name='priority',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='priorities', to='projects.Project', verbose_name='project'),
        ),
        migrations.AddField(
            model_name='membership',
            name='invited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ihaveinvited+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='membership',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='membership',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='users.Role'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issuetype',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_types', to='projects.Project', verbose_name='project'),
        ),
        migrations.AddField(
            model_name='issuestatus',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_statuses', to='projects.Project', verbose_name='project'),
        ),
        migrations.AddField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Category'),
        ),
        migrations.AddField(
            model_name='expense',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='category',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='activity',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='projects.Activity', verbose_name='parent activity'),
        ),
        migrations.AddField(
            model_name='activity',
            name='predecessor',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='predecessors', to='projects.Activity'),
        ),
        migrations.AddField(
            model_name='activity',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.Project', verbose_name='project'),
        ),
        migrations.AddField(
            model_name='activity',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.TaskStatus'),
        ),
        migrations.AddField(
            model_name='activity',
            name='successor',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='successors', to='projects.Activity'),
        ),
        migrations.AlterUniqueTogether(
            name='taskstatus',
            unique_together={('project', 'slug'), ('project', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='severity',
            unique_together={('project', 'name')},
        ),
        migrations.AlterIndexTogether(
            name='project',
            index_together={('name', 'id')},
        ),
        migrations.AlterUniqueTogether(
            name='priority',
            unique_together={('project', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('user', 'project')},
        ),
        migrations.AlterUniqueTogether(
            name='issuetype',
            unique_together={('project', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='issuestatus',
            unique_together={('project', 'slug'), ('project', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together={('project', 'slug'), ('project', 'name')},
        ),
    ]