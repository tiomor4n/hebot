# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-23 23:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=20)),
                ('token', models.CharField(max_length=45)),
                ('verify', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LineInformList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=20)),
                ('nickname', models.CharField(max_length=10)),
                ('token', models.CharField(max_length=45)),
                ('bank', models.CharField(max_length=4)),
                ('BS', models.CharField(max_length=1)),
                ('ccy', models.CharField(max_length=3)),
                ('exrate', models.FloatField(default=0.0)),
                ('stoptoday', models.CharField(max_length=1)),
                ('emailverify', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscribe.EmailVerify')),
            ],
        ),
    ]
