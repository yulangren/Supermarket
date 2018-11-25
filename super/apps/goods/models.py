from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models

# Create your models here.
#   首页轮播图/活动列表模型
from db.base_models import BaseModel

"""
	    商品名称					trade_name
		商品ID						trade_ID
		图片url					url_add
		排序(order	)				priority
		是否轮播					is_carousel
		是否活动					is_activity
		活动地址(URL)				url_activity

"""
class Shuffling_activity(BaseModel):
    trade_naem = models.CharField(max_length=50, verbose_name='商品名称')
    trade_ID = models.ForeignKey(to='Goods_SKU',max_length=20, verbose_name='商品ID')
    img_url_add = models.ImageField(upload_to='goods/%Y%m/%d', verbose_name='图片地址',null=True)
    priority = models.SmallIntegerField(verbose_name='排序',default=0)
    is_carousel = models.BooleanField(choices=((True, '是'), (False, '否')), verbose_name='是否轮播',default=False)
    is_activity = models.BooleanField(choices=((True, '是'), (False, '否')), verbose_name='是否活动',default=False)
    url_activity = models.CharField(max_length=250, verbose_name='活动地址',null=True,default='null')

    # 自定义字段
    def show_img(self):
        return "<img style='width:50px;height:30px' src='{}{}'/>".format(settings.MEDIA_URL,self.img_url_add)
    show_img.allow_tags = True
    show_img.short_description = "img_url"
    def __str__(self):
        return self.trade_naem

    class Meta:
        db_table = 'Shuffling_activity'
        verbose_name = '活动轮播表'
        verbose_name_plural = verbose_name


# 特色专区
"""
        商品名称					trade_name
		商品ID						trade_ID
		描述						describe
		排序(order	)				priority
		是否上架					is_ shelves

"""

# 特色专区
class Features(BaseModel):
    trade_naem = models.CharField(max_length=50, verbose_name='专区名称')
    trade_ID = models.CharField(max_length=20, verbose_name='商品ID')
    describe = models.CharField(max_length=255, verbose_name='商品描述',null=True)
    priority = models.SmallIntegerField(verbose_name='排序',default=0)
    is_shelves = models.BooleanField(choices=((1, '是'), (0, '否')), verbose_name='是否上架',default=1)

    def __str__(self):
        return self.trade_naem

    class Meta:
        db_table = 'features'
        verbose_name = '专区分类表'
        verbose_name_plural = verbose_name


# 专区商品列表(继承基础模型)(多)
# 专区ID					zone_ID
# 商品ID					trade_ID

class Features_list(BaseModel):
    zone_ID = models.ForeignKey(to='Features', verbose_name='专区分类ID')
    trade_ID = models.ForeignKey(to='Goods_SKU',max_length=50, verbose_name='商品SKU_ID')

    def __str__(self):
        return '{}'.format(self.zone_ID)

    class Meta:
        db_table = 'Features_list'
        verbose_name = '专区商品列表'
        verbose_name_plural = verbose_name


# 商品分类
"""
分类名     class_name
分类简介            Introduction
"""

#商品分类
class Goods_class(BaseModel):
    class_name = models.CharField(max_length=30, verbose_name='分类名称')
    introduction = models.CharField(max_length=255, verbose_name='分类简介',null=True)

    def __str__(self):
        return self.class_name

    class Meta:
        db_table = 'goods_class'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name


"""商品SPU表
ID
名称
"""


class Goods_SPU(BaseModel):
    trade_naem = models.CharField(max_length=50, verbose_name='名称')
    trade_ID = RichTextUploadingField(verbose_name='详情')

    def __str__(self):
        return self.trade_naem+self.trade_ID

    class Meta:
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name


"""
图片地址
商品SKUID
"""


# 商品相册

class Photo_album(BaseModel):
    img_url = models.ImageField(upload_to='goods/%Y%m/%d', verbose_name='图片地址')
    trade_ID = models.ForeignKey(to='Goods_SKU', verbose_name='商品ID')

    # 后台显示缩略图
    def img_urls(self):
        return "<img style='width:50px;height:30px' src='{}{}'/>".format(settings.MEDIA_URL,self.img_url)
    img_urls.allow_tags = True
    img_urls.short_description = "img_url"

    def __str__(self):
        return self.trade_ID

    class Meta:
        verbose_name = '商品相册'
        verbose_name_plural = verbose_name



#  单位
class Unit(BaseModel):
    unit_name = models.CharField(max_length=10,verbose_name='单位')
    note = models.CharField(max_length=20,verbose_name='备注')

    def __str__(self):
        return self.unit_name
    class Meta:
        verbose_name = '产品单位'
        verbose_name_plural = verbose_name



"""
商品SKU表
"""
# 商品SKU表
class Goods_SKU(BaseModel):
    goods_name = models.CharField(max_length=100, verbose_name='商品名')
    goods_abstract = models.CharField(max_length=250, verbose_name='商品简介',null=True)
    goods_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')
    goods_unit = models.ForeignKey(to='Unit',verbose_name='单位')
    repertory = models.IntegerField(verbose_name='库存')
    sales = models.SmallIntegerField(verbose_name='销量')
    goods_LOGO = models.ImageField(upload_to='goods/%Y%m', verbose_name='logo地址')
    is_shelves = models.BooleanField(choices=((True, '是'), (False, '否')), verbose_name='是否上架',default=True)
    goods_class = models.ForeignKey(to='Goods_class', verbose_name='商品分类ID')
    goods_spu = models.ForeignKey(to='Goods_SPU', verbose_name='商品SPU_id')

    # 自定义字段
    def show_logo(self):
        return "<img style='width:50px;height:30px' src='{}{}'/>".format(settings.MEDIA_URL,self.goods_LOGO)
    show_logo.allow_tags = True
    show_logo.short_description = "img_url"

    def __str__(self):
        return self.goods_name

    class Meta:
        verbose_name = '商品SKU表'
        verbose_name_plural = verbose_name


