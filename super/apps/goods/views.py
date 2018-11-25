from django.shortcuts import render,redirect


# 首页
from goods.models import Shuffling_activity, Goods_SKU, Goods_class, Features, Features_list


def index(request):
    shuffling = Shuffling_activity.objects.filter(is_carousel=True,is_delete = False)      # 轮播图
    activity = Shuffling_activity.objects.filter(is_activity=True, is_delete = False).order_by('-priority')      # 活动列表
    lists= Goods_class.objects.first().pk       # 得到分类列表的ID
    Feat = Features.objects.all()       # 专区分类
    context = {'shuffling':shuffling,'activity':activity,'lists':lists,'Feat':Feat}     # 参数传递
    return render(request,'index.html',context)
# 模型类中没有明确的外键时,逆向方法(模型对象.别模型类_set.属性),有明确外键时,正向方法(模型对象.外键属性.别类的属性



# 列表页
def category(request,go_id,order):
    order = int(order)      # 列表ID
    go_id = int(go_id)      # 排序方式
    goods = Goods_class.objects.all()       # 查询分类名
    order_by = ['id','sales','-goods_price','goods_price','-create_date']       # pk , 价格降序,价格升序,时间倒序

    # 从分类列表中取出一个对象
    try:
        goods_get = Goods_class.objects.get(id=go_id)
    except:
        goods_get = Goods_class.objects.get(id=1).pk
            # 如果输入的值为非法或不正确,就给一个默认值

    goods_sku = Goods_SKU.objects.filter(goods_class_id=goods_get).order_by(order_by[order])          # 查询所有的产品
    #         对查询的记录进行相应的排序控制

    context = {'goods':goods,
               'go_id':go_id,
               'goods_get':goods_get,
               'goods_sku':goods_sku,
               'order':order
               }     # 参数传递

    return render(request,'category.html',context)




# 商品详情页
def detail(request,id):
    try:
        id = int(id)
        SKU = Goods_SKU.objects.get(id=id)
    except:
        return redirect('goods:index')
    return render(request,'detail.html',{'sku':SKU})