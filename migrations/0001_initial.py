# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='日期')),
                ('bandwidth', models.BigIntegerField(verbose_name='带宽')),
            ],
        ),
        migrations.CreateModel(
            name='In',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='日期')),
                ('num', models.DecimalField(decimal_places=2, verbose_name='金额', max_digits=10)),
                ('memo', models.CharField(max_length=256, verbose_name='备注', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Out',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('log', models.CharField(max_length=256, verbose_name='记录')),
                ('date', models.DateField(verbose_name='日期')),
                ('num', models.DecimalField(decimal_places=2, verbose_name='金额', max_digits=10)),
                ('memo', models.CharField(max_length=256, verbose_name='备注', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('status', models.BooleanField(verbose_name='状态', default=False)),
                ('port', models.IntegerField(unique=True, verbose_name='端口')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('setup_date', models.DateField(verbose_name='建立日期')),
                ('end_date', models.DateField(verbose_name='结束日期')),
                ('memo', models.CharField(max_length=256, verbose_name='备注', null=True, blank=True)),
                ('user', models.OneToOneField(verbose_name='用户', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='in',
            name='user',
            field=models.ForeignKey(to='panel.User', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='flow',
            name='user',
            field=models.OneToOneField(verbose_name='用户', to=settings.AUTH_USER_MODEL),
        ),
    ]
