# Generated by Django 2.0.5 on 2018-05-29 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_auto_20180526_1311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('id',)},
        ),
        migrations.AlterIndexTogether(
            name='project',
            index_together=set(),
        ),
    ]