from django.shortcuts import render,redirect

# 购物车的点击添加
from django.views import View
from django_redis import get_redis_connection
from django.http import JsonResponse,HttpResponse

from db.login_session import Session
from goods.models import Goods_SKU


class Cart(View):
    def get(self,request):
        return HttpResponse('显示')

    def post(self,request):

        sku_id = request.POST.get('sku_id')     # 获取商品skuID
        count = request.POST.get('count')        # 获取添加数量
        # 转为整型
        sku_id=int(sku_id)
        count=int(count)

        # 判断是否登陆,
        user_id = request.session.get('id')     #
        if user_id is None:
            return JsonResponse({"con":0,'hint':'未登录'})      # 未登陆

        # 判断商品id是否存在
        if sku_id not in [int(i.pk) for i in Goods_SKU.objects.all()]:
            #  取商品 id: 遍历出所有的记录,然后再拿出记录的id
            return JsonResponse({'con':1,'hint':'商品不存在'})          # 商品id非法或不存在

        # if count<= 0:
        #     return JsonResponse({'con':2,'hint':'数量异常'})          # 数量错误

        data = Goods_SKU.objects.get(id=sku_id)     # 创建商品对象
        if count > data.repertory:  # 获取商品的库存
            return JsonResponse({'con':3,'hint':'库存不足'})  #   库存不足
        else:
            # 保存至Redis数据库
            r = get_redis_connection(alias='default')   #   创建Redis对象
            if all([user_id,sku_id,count]):
                res = r.hincrby(user_id,sku_id,count) #  添加为哈希类型数据,分别为: 用户ID/商品ID/数量
                if res == 0:
                    r.hdel(user_id,sku_id)      # 当商品数量为0时, 删除词条记录
            re = r.hgetall(user_id)          # 查询数据
            val = 0
            for k,v in re.items():
                v = int(v.decode('utf-8'))
                val += v
            return JsonResponse({'con':200,'values':val})








# 购物车

class ShopCart(View):
    def get(self,request):
        if  request.session.get('id'):   # 已登陆
            #  回显商品数据,从redis中获取商品信息
            r = get_redis_connection('default')     # 创建Redis连接
            user_id = request.session.get('id')
            sku_id_count = r.hgetall(user_id)       # 获取商品的sku 和 商品的数量
            goods = []      # 准备一个空列表,用于存放遍历后的商品对象
            for sku_id, count in sku_id_count.items():
                 # sku_id = int(sku_id)        #    默认数据是二进制,强转换成整数
                 # count = int(count)
                goods_sku = Goods_SKU.objects.get(pk=sku_id,is_delete=False,is_shelves=True)   # 筛选出未删除及未下架发商品
                goods_sku.count = count     # 将商品数量添加为sku的属性
                goods.append(goods_sku)     # 追加到列表
            context = {'goods_sku':goods}
            return render(request,'shopcart.html',context)
        else:
            return redirect('user:login')   # 当为登陆时,跳转至登陆页面


    def post(self,request):
        pass