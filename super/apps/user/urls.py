from django.conf.urls import url

from user.views import member, reg, login, ForgetPassword, infor, Quit, verification, integral, cash, obligation

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
]