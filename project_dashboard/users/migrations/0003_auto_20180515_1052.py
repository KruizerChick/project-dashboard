# Generated by Django 2.0.5 on 2018-05-15 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20180515_1052'),
        ('users', '0002_auto_20180514_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=250, verbose_name='slug')),
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
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AddField(
            model_name='user',
            name='timezone',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='default timezone'),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together={('slug', 'project')},
        ),
    ]
