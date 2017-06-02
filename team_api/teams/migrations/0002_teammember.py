# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-02 20:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False, help_text="Admin members are allowed to edit the team's information, as well as change player info.", verbose_name='Is admin')),
                ('member_type', models.PositiveSmallIntegerField(choices=[(0, 'Coach'), (1, 'Player')], default=1, verbose_name='Member type')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='teams.Team', verbose_name='Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
