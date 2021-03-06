# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-06 02:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_teaminvite'),
    ]

    operations = [
        migrations.AddField(
            model_name='teaminvite',
            name='invite_accept_url',
            field=models.URLField(default='example.com/invites', help_text='The URL where the user can go to accept the invitation.', verbose_name='invite accept URL'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teaminvite',
            name='signup_url',
            field=models.URLField(default='example.com/signup', help_text='The URL where the user can go to sign up for an account.', verbose_name='signup url'),
            preserve_default=False,
        ),
    ]
