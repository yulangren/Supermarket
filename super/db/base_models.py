from django.db import models
class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    create_date = models.DateField(auto_now_add=True, verbose_name='注册时间')  # 注册日期
    update_data = models.DateField(auto_now=True, verbose_name='修改时间')  # 修改时间

    class Meta:
        abstract= True   # 只能被继承与实例,不可迁移