# Generated by Django 2.0.5 on 2018-05-24 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20180524_1354'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issueprogress',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='resolved',
            field=models.DateField(blank=True, null=True, verbose_name='date completed'),
        ),
    ]