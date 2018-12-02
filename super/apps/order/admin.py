from django.contrib import admin

# Register your models here.
from order.models import ModeTransport, OrderStatus, OrderCommodity, PaymentMethod


#  运输方式管理
@admin.register(ModeTransport)
class ModeTransport(admin.ModelAdmin):
    pass


# 订单信息
@admin.register(OrderStatus)
class OrderStatus(admin.ModelAdmin):
    list_display = ['userID', 'address_name', 'order_state', 'address_note', 'transport', 'order_number', 'order_money']


# 付款方式
@admin.register(PaymentMethod)
class PaymentMethod(admin.ModelAdmin):
    list_display = ['payment_name', 'payment_img']


# 订单商品表
@admin.register(OrderCommodity)
class OrderCommodity(admin.ModelAdmin):
    list_display = ['skuID', 'oderId', 'goods_count', 'goods_price']
