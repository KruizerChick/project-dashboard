# Generated by Django 2.0.5 on 2018-05-15 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180515_1052'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_auto_20180515_1052'),
    ]

    operations = [
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
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('user', 'project')},
        ),
    ]