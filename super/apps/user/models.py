from django.db import models

from db.base_models import BaseModel        # 继承基础数据模型

# 会员模型表

class Members(BaseModel):
    user_ID = models.CharField(max_length=11, unique=True, verbose_name='手机')  # 手机
    user_sex = models.SmallIntegerField(choices=((1, '男'), (2, '女')), default=1, verbose_name='性别')  # 性别
    nick_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='昵称')  # 昵称
    borm_date = models.DateField(null=True, blank=True, verbose_name='出生日期')  # 出生日期
    school = models.CharField(max_length=50, null=True, blank=True, verbose_name='学校')  # 学校
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='地址')  # 地址
    hometown = models.CharField(max_length=20, null=True, blank=True, verbose_name='故乡')  # 故乡
    password = models.CharField(max_length=64, verbose_name='密码')  # 账户密码
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, verbose_name='余额')  # 账号余额
    integral = models.IntegerField(default=0, null=True, verbose_name='积分')  # 积分
    coupons = models.SmallIntegerField(default=0,null=True, verbose_name='优惠券')  # 优惠券
    collection = models.IntegerField(default=0, null=True, verbose_name='收藏')  # 收藏
    head_portrait = models.ImageField(upload_to= 'head/logo', null=True, verbose_name='头像')  # 头像
    pay_password = models.CharField(max_length=64, null=True, blank=True, verbose_name='支付密码')  # 支付密码


    def __str__(self):
        return self.nick_name

    class Meta:
        db_table = 'Members'  # 数据表名
        verbose_name = '用户管理'
        verbose_name_plural=verbose_name
