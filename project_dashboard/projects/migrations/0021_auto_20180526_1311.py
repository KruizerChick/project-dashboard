# Generated by Django 2.0.5 on 2018-05-26 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20180526_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='stakeholder',
            name='full_name',
            field=models.CharField(default='change', help_text="Stakeholder's full name", max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stakeholder',
            name='title',
            field=models.CharField(blank=True, max_length=100, verbose_name='job title'),
        ),
    ]
