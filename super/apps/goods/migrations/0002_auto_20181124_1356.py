# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-24 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods_sku',
            name='goods_unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='goods.Unit', verbose_name='单位'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='goods_spu',
            name='trade_ID',
            field=models.TextField(default='', max_length=255, verbose_name='详情'),
        ),
    ]
