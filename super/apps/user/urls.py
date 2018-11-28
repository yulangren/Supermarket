from django.conf.urls import url

from user.views import member, reg, login, ForgetPassword, infor, Quit, verification, integral, cash, obligation, \
    Gladdress, Address, address_edit, address_del, default_edit

urlpatterns=[
    url(r'^$',member,name='member'),      # 个人中心
    url(r'^reg/$',reg,name='reg'),      # 会员注册
    url(r'^login/$',login,name='login'),      # 会员登录
    url(r'^getpassword/$',ForgetPassword.as_view(),name='ForgetPassword'),      # 找回密码
    url(r'^infor/$',infor,name='infor'), # 个人资料
    url(r'^quit/$',Quit,name='quit'), # 退出登录
    url(r'^integral/$',integral,name='integral'), # 积分
    url(r'^integral/cash/$',cash,name='cash'), # 积分兑换
    url(r'^obligation/$',obligation,name='obligation'), # 待付款
    url(r'^verification/$',verification,name='verification'), # 退出登录
    url(r'^address/$',Address.as_view(),name='address'), # 地址添加页
    url(r'^gladdress/$',Gladdress.as_view(),name='gladdress'), # 收货地址管理
    url(r'^gladdress/edit/$',address_edit,name='address_edit'), # 收货地址修改
    url(r'^gladdress/address_del/$',address_del,name='address_del'), # 删除收货地址
    url(r'^gladdress/default_edit/$',default_edit,name='default_edit'), # 修改默认收货地址
]