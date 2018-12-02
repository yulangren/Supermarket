# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-02 09:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20181130_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modetransport',
            name='carriage_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='价格'),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='actually_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='实付金额'),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='address_note',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='备注说明'),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='order_money',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='订单金额'),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='order_state',
            field=models.SmallIntegerField(choices=[(0, '待付款'), (1, '退发货'), (2, '待收货'), (3, '待评价'), (4, '已完成'), (5, '已付款'), (6, '已退货'), (7, '已评价')], verbose_name='订单状态'),
        ),
        migrations.AlterField(
            model_name='orderstatus',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.PaymentMethod', verbose_name='付款方式'),
        ),
    ]
