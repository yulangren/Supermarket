from django.conf.urls import url

from user.views import member

urlpatterns=[
    url(r'^member/$',member,name='member')      # 绑定会员
]