# Generated by Django 2.0.5 on 2018-05-23 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20180523_0912'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membership',
            options={'ordering': ['project', 'stakeholder__full_name', 'stakeholder__user', 'stakeholder__email_address'], 'verbose_name': 'membership', 'verbose_name_plural': 'memberships'},
        ),
    ]
