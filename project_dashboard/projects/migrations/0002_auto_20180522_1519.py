# Generated by Django 2.0.5 on 2018-05-22 20:19

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=250, verbose_name='slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('permissions', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(choices=[('view_project', 'View project'), ('view_milestones', 'View milestones'), ('add_milestone', 'Add milestone'), ('modify_milestone', 'Modify milestone'), ('delete_milestone', 'Delete milestone'), ('view_epics', 'View epic'), ('add_epic', 'Add epic'), ('modify_epic', 'Modify epic'), ('comment_epic', 'Comment epic'), ('delete_epic', 'Delete epic'), ('view_us', 'View user story'), ('add_us', 'Add user story'), ('modify_us', 'Modify user story'), ('comment_us', 'Comment user story'), ('delete_us', 'Delete user story'), ('view_tasks', 'View tasks'), ('add_task', 'Add task'), ('modify_task', 'Modify task'), ('comment_task', 'Comment task'), ('delete_task', 'Delete task'), ('view_issues', 'View issues'), ('add_issue', 'Add issue'), ('modify_issue', 'Modify issue'), ('comment_issue', 'Comment issue'), ('delete_issue', 'Delete issue'), ('view_wiki_pages', 'View wiki pages'), ('add_wiki_page', 'Add wiki page'), ('modify_wiki_page', 'Modify wiki page'), ('comment_wiki_page', 'Comment wiki page'), ('delete_wiki_page', 'Delete wiki page'), ('view_wiki_links', 'View wiki links'), ('add_wiki_link', 'Add wiki link'), ('modify_wiki_link', 'Modify wiki link'), ('delete_wiki_link', 'Delete wiki link')]), blank=True, default=[], null=True, size=None, verbose_name='permissions')),
                ('role_type', models.CharField(choices=[('I', 'Internal'), ('E', 'External')], default='I', help_text='Relative to the project team.', max_length=1)),
                ('order', models.IntegerField(default=10, verbose_name='order')),
                ('computable', models.BooleanField(default=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='projects.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
                'ordering': ['order', 'slug'],
            },
        ),
        migrations.CreateModel(
            name='Stakeholder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('full_name', models.CharField(blank=True, max_length=100)),
                ('email_address', models.EmailField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('organization', models.CharField(blank=True, help_text='(Optional) Company, business unit or department.', max_length=100)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128)),
                ('impact', models.IntegerField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], default=1)),
                ('influence', models.IntegerField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], default=1)),
                ('risk_tolerance', models.IntegerField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], default=1)),
                ('needs', models.TextField(blank=True, help_text='Items that are NOT OPTIONAL for this Stakeholder.', null=True)),
                ('wants', models.TextField(blank=True, help_text='Items that are OPTIONAL for this Stakeholder.', null=True)),
                ('expectations', models.TextField(blank=True, help_text='Unusual or emphatic expectations that need to be noted.', null=True)),
                ('strategy', models.TextField(blank=True, help_text='Strategies and tactics to maximize positive influence and minimize negative influence.', null=True)),
                ('project', models.ForeignKey(help_text='Belongs to this project.', on_delete=django.db.models.deletion.CASCADE, related_name='stakeholders', to='projects.Project')),
                ('user', models.OneToOneField(blank=True, help_text='(Optional) Link to User if available', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'stakeholder',
                'ordering': ['-influence', '-impact'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together={('slug', 'project')},
        ),
    ]