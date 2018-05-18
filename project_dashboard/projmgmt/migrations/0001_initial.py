# Generated by Django 2.0.5 on 2018-05-17 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(help_text="Used to build the knowledge area's URL.", max_length=100, unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(help_text="Used to build the process' URL.", max_length=100, unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('knowledge_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processes', to='projmgmt.KnowledgeArea', verbose_name='knowledge area')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
        ),
        migrations.AddField(
            model_name='process',
            name='process_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processes', to='projmgmt.ProcessGroup', verbose_name='process group'),
        ),
    ]