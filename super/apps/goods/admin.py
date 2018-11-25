from django.contrib import admin

from goods.models import Shuffling_activity, Features, Photo_album, Goods_SPU, Goods_class, Features_list, Goods_SKU, \
    Unit


# 注册轮播图
@admin.register(Shuffling_activity)
class Shuffling_activity(admin.ModelAdmin):
    list_per_page=10     # 每页显示的条数
    list_display_links = ['trade_naem']
    list_filter = ['is_carousel']      # 右边栏 过滤器
    search_fields = ['trade_naem']                # 搜索
    list_display = ['id','trade_naem','show_img','priority','is_carousel','is_activity','url_activity'] # 显示列表的字段



# 特色专区
@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_per_page = 5           # 每页显示五条
    actions_on_top = True           # 操作按钮显示在上面
    list_display_links = ['id','trade_naem']
    list_display = ['id', 'trade_naem', 'priority', 'is_shelves']       # 显示列表的字段


# 商品相册
@admin.register(Photo_album)
class Photo_album(admin.ModelAdmin):
    list_display_links = ['trade_ID','img_urls']
    list_display = ['trade_ID','img_urls']


# 商品SPU表
@admin.register(Goods_SPU)
class Goods_SPU(admin.ModelAdmin):
    pass

# 商品分类表
@admin.register(Goods_class)
class Goods_class(admin.ModelAdmin):
    pass
# 专区商品分类表
@admin.register(Features_list)
class Features_list(admin.ModelAdmin):
    list_display = ['zone_ID','trade_ID']



# 商品SKU表
@admin.register(Goods_SKU)
class Goods_SKU(admin.ModelAdmin):
    list_display_links = ['goods_name']
    list_display = ['id', 'goods_name', 'goods_price', 'repertory','sales','show_logo','goods_class','is_shelves']


#  单位
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['id','unit_name']