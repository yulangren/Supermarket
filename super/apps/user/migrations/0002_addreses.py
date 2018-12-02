# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-28 08:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Addreses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='注册时间')),
                ('update_data', models.DateField(auto_now=True, verbose_name='修改时间')),
                ('take_user', models.CharField(max_length=20, verbose_name='收件人')),
                ('detail_address', models.CharField(max_length=150, verbose_name='详细地址')),
                ('province', models.CharField(max_length=5, verbose_name='省')),
                ('city', models.CharField(max_length=10, verbose_name='市')),
                ('district', models.CharField(max_length=10, verbose_name='区')),
                ('tel_sign', models.CharField(max_length=11, verbose_name='联系电话')),
                ('is_default', models.BooleanField(choices=[(True, '是'), (False, '否')], default=False, verbose_name='是否默认地址')),
                ('add_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Members', verbose_name='创建人')),
            ],
            options={
                'verbose_name': '会员收货地址管理',
                'verbose_name_plural': '会员收货地址管理',
                'db_table': 'address',
            },
        ),
    ]