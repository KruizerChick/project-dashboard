# Generated by Django 2.0.5 on 2018-05-18 17:40

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import project_dashboard.core.utils.time


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=255, verbose_name='slug')),
                ('description', models.TextField(blank=True, help_text='Description of activity or task.', verbose_name='description')),
                ('order', models.IntegerField(default=10, verbose_name='order')),
                ('is_closed', models.BooleanField(default=False, verbose_name='is closed')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'verbose_name': 'activiy',
                'verbose_name_plural': 'activities',
                'ordering': ['project', 'order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'ordering': ('-amount',),
            },
        ),
        migrations.CreateModel(
            name='IssueStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=255, verbose_name='slug')),
                ('order', models.IntegerField(default=10, verbose_name='order')),
                ('is_closed', models.BooleanField(default=False, verbose_name='is closed')),
                ('color', models.CharField(default='#999999', max_length=20, verbose_name='color')),
            ],
            options={
                'verbose_name': 'issue status',
                'verbose_name_plural': 'issue statuses',
                'ordering': ['project', 'order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='IssueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('order', models.IntegerField(default=10, verbose_name='order')),
                ('color', models.CharField(default='#999999', max_length=20, verbose_name='color')),
            ],
            options={
                'verbose_name': 'issue type',
                'verbose_name_plural': 'issue types',
                'ordering': ['project', 'order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, default=None, max_length=255, null=True, verbose_name='email')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='create at')),
                ('token', models.CharField(blank=True, default=None, max_length=60, null=True, verbose_name='token')),
                ('invitation_extra_text', models.TextField(blank=True, null=True, verbose_name='invitation extra text')),
                ('user_order', models.BigIntegerField(default=project_dashboard.core.utils.time.timestamp_ms, verbose_name='user order')),
            ],
            options={
                'verbose_name': 'membership',
                'verbose_name_plural': 'memberships',
                'ordering': ['project', 'user__full_name', 'user__username', 'user__email', 'email'],
            },
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('order', models.IntegerField(default=10, verbose_name='order')),
                ('color', models.CharField(default='#999999', max_length=20, verbose_name='color')),
            ],
            options={
                'verbose_name': 'priority',
                'verbose_name_plural': 'priorities',
                'ordering': ['project', 'order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='project')),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('description', models.TextField(verbose_name='description')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date modified')),
                ('total_milestones', models.IntegerField(blank=True, null=True, verbose_name='total of milestones')),
                ('is_contact_activated', models.BooleanField(default=True, verbose_name='active contact')),
                ('is_backlog_activated', models.BooleanField(default=True, verbose_name='active backlog panel')),
                ('is_kanban_activated', models.BooleanField(default=False, verbose_name='active kanban panel')),
                ('is_wiki_activated', models.BooleanField(default=True, verbose_name='active wiki panel')),
                ('is_issues_activated', models.BooleanField(default=True, verbose_name='active issues panel')),
                ('is_private', models.BooleanField(default=True, verbose_name='is private')),
                ('anon_permissions', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(choices=[('view_project', 'View project'), ('view_milestones', 'View milestones'), ('view_epics', 'View epic'), ('view_us', 'View user stories'), ('view_tasks', 'View tasks'), ('view_issues', 'View issues'), ('view_wiki_pages', 'View wiki pages'), ('view_wiki_links', 'View wiki links')]), blank=True, default=[], null=True, size=None, verbose_name='anonymous permissions')),
                ('public_permissions', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(choices=[('view_project', 'View project'), ('view_milestones', 'View milestones'), ('add_milestone', 'Add milestone'), ('modify_milestone', 'Modify milestone'), ('delete_milestone', 'Delete milestone'), ('view_epics', 'View epic'), ('add_epic', 'Add epic'), ('modify_epic', 'Modify epic'), ('comment_epic', 'Comment epic'), ('delete_epic', 'Delete epic'), ('view_us', 'View user story'), ('add_us', 'Add user story'), ('modify_us', 'Modify user story'), ('comment_us', 'Comment user story'), ('delete_us', 'Delete user story'), ('view_tasks', 'View tasks'), ('add_task', 'Add task'), ('modify_task', 'Modify task'), ('comment_task', 'Comment task'), ('delete_task', 'Delete task'), ('view_issues', 'View issues'), ('add_issue', 'Add issue'), ('modify_issue', 'Modify issue'), ('comment_issue', 'Comment issue'), ('delete_issue', 'Delete issue'), ('view_wiki_pages', 'View wiki pages'), ('add_wiki_page', 'Add wiki page'), ('modify_wiki_page', 'Modify wiki page'), ('comment_wiki_page', 'Comment wiki page'), ('delete_wiki_page', 'Delete wiki page'), ('view_wiki_links', 'View wiki links'), ('add_wiki_link', 'Add wiki link'), ('modify_wiki_link', 'Modify wiki link'), ('delete_wiki_link', 'Delete wiki link')]), blank=True, default=[], null=True, size=None, verbose_name='user permissions')),
                ('tasks_csv_uuid', models.CharField(blank=True, db_index=True, default=None, editable=False, max_length=32, null=True)),
                ('issues_csv_uuid', models.CharField(blank=True, db_index=True, default=None, editable=False, max_length=32, null=True)),
                ('totals_updated_datetime', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='updated date time')),
                ('total_activity', models.PositiveIntegerField(db_index=True, default=0, verbose_name='count')),
                ('total_activity_last_week', models.PositiveIntegerField(db_index=True, default=0, verbose_name='activity last week')),
                ('total_activity_last_month', models.PositiveIntegerField(db_index=True, default=0, verbose_name='activity last month')),
                ('total_activity_last_year', models.PositiveIntegerField(db_index=True, default=0, verbose_name='activity last year')),
                ('budget', models.IntegerField(help_text='Amount allocated to this project.', verbose_name='budget')),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
                'ordering': ['name', 'id'],
            },
        ),
        migrations.CreateModel(
            name='ProjectTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True, verbose_name='slug')),
                ('description', models.TextField(verbose_name='description')),
                ('order', models.BigIntegerField(default=project_dashboard.core.utils.time.timestamp_ms, verbose_name='user order')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created date')),
                ('modified_date', models.DateTimeField(verbose_name='modified date')),
                ('default_owner_role', models.CharField(max_length=50, verbose_name="default owner's role")),
                ('is_contact_activated', models.BooleanField(default=True, verbose_name='active contact')),
                ('is_backlog_activated', models.BooleanField(default=True, verbose_name='active backlog panel')),
                ('is_kanban_activated', models.BooleanField(default=False, verbose_name='active kanban panel')),
                ('is_wiki_activated', models.BooleanField(default=True, verbose_name='active wiki panel')),
                ('is_issues_activated', models.BooleanField(default=True, verbose_name='active issues panel')),
                ('default_options', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='default options')),
                ('epic_statuses', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='epic statuses')),
                ('us_statuses', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='us statuses')),
                ('points', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='points')),
                ('task_statuses', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='task statuses')),
                ('issue_statuses', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='issue statuses')),
                ('issue_types', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='issue types')),
                ('priorities', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='priorities')),
                ('severities', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='severities')),
                ('roles', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='roles')),
                ('epic_custom_attributes', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='epic custom attributes')),
                ('us_custom_attributes', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='us custom attributes')),
                ('task_custom_attributes', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='task custom attributes')),
                ('issue_custom_attributes', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='issue custom attributes')),
            ],
            options={
                'verbose_name': 'project template',
                'verbose_name_plural': 'project templates',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Severity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('order', models.IntegerField(default=10, verbose_name='order')),
                ('color', models.CharField(default='#999999', max_length=20, verbose_name='color')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='severities', to='projects.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'severity',
                'verbose_name_plural': 'severities',
                'ordering': ['project', 'order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=255, verbose_name='slug')),
                ('order', models.IntegerField(default=10, verbose_name='order')),
                ('is_closed', models.BooleanField(default=False, verbose_name='is closed')),
                ('color', models.CharField(default='#999999', max_length=20, verbose_name='color')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_statuses', to='projects.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'task status',
                'verbose_name_plural': 'task statuses',
                'ordering': ['project', 'order', 'name'],
            },
        ),
        migrations.AddField(
            model_name='project',
            name='creation_template',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='projects.ProjectTemplate', verbose_name='creation template'),
        ),
        migrations.AddField(
            model_name='project',
            name='default_issue_status',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='projects.IssueStatus', verbose_name='default issue status'),
        ),
        migrations.AddField(
            model_name='project',
            name='default_issue_type',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='projects.IssueType', verbose_name='default issue type'),
        ),
        migrations.AddField(
            model_name='project',
            name='default_priority',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='projects.Priority', verbose_name='default priority'),
        ),
        migrations.AddField(
            model_name='project',
            name='default_severity',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='projects.Severity', verbose_name='default severity'),
        ),
        migrations.AddField(
            model_name='project',
            name='default_task_status',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='projects.TaskStatus', verbose_name='default task status'),
        ),
    ]
