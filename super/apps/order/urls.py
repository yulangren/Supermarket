"""super URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from order.views import tureorder, order_pay, order_all, pay, star

urlpatterns = [
    url(r'^tureorder/$',tureorder,name='tureorder') ,    # 提交订单
    url(r'^tureorder/pay/$',order_pay,name='order_pay'),     # 确认订单
    url(r'^allorder/$',order_all,name='order_all'),     # 全部订单
    url(r'^pay/',pay,name='pay'),     # 确认支付
    url(r'^pay_star/',star,name='star'),     # 支付结果
]
