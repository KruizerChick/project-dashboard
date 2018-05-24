# Generated by Django 2.0.5 on 2018-05-23 19:32

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20180523_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=255, verbose_name='slug')),
                ('description', models.TextField(blank=True, help_text='Description of activity or task.', verbose_name='description')),
                ('order', models.IntegerField(default=10, verbose_name='order')),
                ('status', models.CharField(blank=True, choices=[(0, 'Not Started'), (1, 'In Progress'), (2, 'Completed')], default=0, max_length=7, null=True)),
                ('is_closed', models.BooleanField(default=False, verbose_name='is closed')),
                ('is_milestone', models.BooleanField(default=False, verbose_name='is milestone')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='projects.Task', verbose_name='parent activity')),
                ('predecessor', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='predecessors', to='projects.Task')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects.Project', verbose_name='project')),
                ('resources', models.ManyToManyField(related_name='tasks', to='projects.Stakeholder', verbose_name='resources')),
                ('successor', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='successors', to='projects.Task')),
            ],
            options={
                'verbose_name': 'task',
                'ordering': ['project', 'order', 'name'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together={('project', 'name'), ('project', 'slug')},
        ),
    ]