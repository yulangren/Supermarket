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
from django.conf.urls import url, include
from django.contrib import admin

import user
from goods.views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index,name='首页'),   # 网站首页
    # 全文搜索框架
    url(r'^search/', include('haystack.urls')),
    # 上传部件自动调用的上传地址
    url(r'^ckeditor/', include("ckeditor_uploader.urls")),
    # 其他模块
    url(r'^member/',include('user.urls',namespace='user')) ,       # 用户模块(user)
    url(r'^goods/',include('goods.urls',namespace='goods')) ,       # 商品模块(goods)
    url(r'^Cart/',include('cart.urls',namespace='cart')) ,       # 购物车(Cart)
    url(r'^order/',include('order.urls',namespace='order')) ,       # 订单(order)
]
