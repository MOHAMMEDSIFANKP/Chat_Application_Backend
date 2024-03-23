# Generated by Django 5.0.3 on 2024-03-23 12:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_friendslist'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendslist',
            unique_together={('user_id', 'friends_id')},
        ),
    ]