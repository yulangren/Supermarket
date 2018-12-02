from django.db import models

from db.base_models import BaseModel


# 订单信息表
class OrderStatus(BaseModel):
    order_number = models.CharField(max_length=64, verbose_name='订单编号')
    order_money = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='订单金额')
    userID = models.CharField(max_length=30, verbose_name='用户ID')
    address_name = models.CharField(max_length=30, verbose_name='收货人姓名')
    address_tel = models.CharField(max_length=11, verbose_name='收货人电话')
    address_site = models.CharField(max_length=150, verbose_name='订单地址')
    order_state = models.SmallIntegerField(choices=((0, '待付款'), (1, '退发货'),
                                               (2, '待收货'), (3, '待评价'),
                                               (4, '已完成'),(5,'已付款'),(6,'已退货'),(7, '已评价')), verbose_name='订单状态'
                                      )
    transport = models.ForeignKey(to='ModeTransport', verbose_name='运输方式')
    payment_method = models.ForeignKey(to='PaymentMethod', blank=True, null=True, verbose_name='付款方式')
    actually_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='实付金额')
    address_note = models.CharField(max_length=255, null=True, blank=True, verbose_name='备注说明')

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name = '订单信息表'
        verbose_name_plural = verbose_name


# 运输方式
class ModeTransport(BaseModel):
    carriage_name = models.CharField(max_length=20, verbose_name='名称')
    carriage_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='价格')

    def __str__(self):
        return self.carriage_name

    class Meta:
        verbose_name = '运输方式'
        verbose_name_plural = verbose_name


# 付款方式
class PaymentMethod(BaseModel):
    payment_name = models.CharField(max_length=20, verbose_name='名称')
    payment_img = models.ImageField(upload_to='order')

    def __str__(self):
        return self.payment_name

    class Meta:
        verbose_name = '付款方式'
        verbose_name_plural = verbose_name


# 订单商品表
class OrderCommodity(BaseModel):
    oderId = models.ForeignKey(to='OrderStatus', verbose_name='订单ID')
    skuID = models.ForeignKey(to='goods.Goods_SKU', verbose_name='商品sku_ID')
    goods_count = models.SmallIntegerField(verbose_name='商品数量')
    goods_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')

    def __str__(self):
        return self.oderId.address_name

    class Meta:
        verbose_name = '订单商品表'
        verbose_name_plural = verbose_name
