import datetime
import os

from alipay import AliPay
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# 提交订单
from db.login_session import Session
from goods.models import Goods_SKU
from django_redis import get_redis_connection
import time
from django.conf import settings

from order.models import ModeTransport, OrderStatus, OrderCommodity, PaymentMethod
from user.models import Addreses, Members


# 提交订单,生成
@Session
def tureorder(request):
    r = get_redis_connection('default')

    #  接收参数
    sku_ids = request.GET.getlist('sku_id')  # 多个相同名字的值用getlist  得到的是一个列表
    #  创建redis对象
    user_id = request.session.get('id')
    goods_sku = []
    # 回显数据
    for sku_id in sku_ids:
        count = int(r.hget(user_id, sku_id))
        sku = Goods_SKU.objects.get(pk=sku_id, is_delete=False)
        sku.count = count  # 获取Redis数据库的商品数量 添加属性到sku
        goods_sku.append(sku)

    user_addr = Addreses.objects.filter(add_user=Members.objects.get(user_ID=request.session.get('id')).pk,
                                        is_delete=False).order_by('is_default').first()  # 取一个
    # 获取运输方式
    transport = ModeTransport.objects.filter()

    # 渲染数据
    context = {'goods_sku': goods_sku, 'user_addr': user_addr, 'transport': transport}
    return render(request, 'tureorder.html', context)


# 事务装饰器
@transaction.atomic
# 确认订单
@Session
def order_pay(request):
    r = get_redis_connection('default')
    # ajax
    if request.method == "POST":
        #  接收参数
        sku_id = request.POST.getlist('sku_id')  # sku_id      字符串
        transport_mode = int(request.POST.get('transport_mode'))  # 运输方式
        remark = request.POST.get('remark')  # 备注
        direction = int(request.POST.get('direction'))  # 收货人ID

        #  获取当前用户
        user = request.session.get('id')

        # 验证参数是否接收完整
        if not all([sku_id, direction, transport_mode]):
            return JsonResponse({"star": 0, "error": "参数错误"})
        # 验证sku商品是否存在
        try:
            for sku in sku_id:
                sku = int(sku)
                Goods_SKU.objects.get(pk=sku, is_delete=False)  # 验证sku商品是否存在,如果不存在,就抛出异常
        except Goods_SKU.DoesNotExist:
            return JsonResponse({"star": 1, "error": "参数错误"})

        #  判断运输方式是否正常
        try:
            transport = ModeTransport.objects.get(pk=int(transport_mode), is_delete=False)
        except ModeTransport.DoesNotExist:
            return JsonResponse({"star": 2, "error": "运输方式错误"})

        # 收货人是否存在
        try:
            sites = Addreses.objects.get(pk=int(direction), is_delete=False)  # 一个对象
        except Addreses.DoesNotExist:
            return JsonResponse({"star": 3, "error": "收货人地址"})

        # 验证用户是否正确
        try:
            user_id = Members.objects.get(user_ID=user, is_delete=False).pk
        except Members.DoesNotExist:
            return JsonResponse({"star": 4, "error": "用户不存在"})

        # 查询商品数量
        try:
            for sku in sku_id:
                count = int(r.hget(user, sku))
                goods_sku = Goods_SKU.objects.get(pk=sku, is_delete=False).repertory
                if count > goods_sku:
                    return JsonResponse({"star": 9, "error": "商品数量不足"})

        except:
            return JsonResponse({"star": 9, "error": "商品数量不足"})

        # 准备其他数据
        # 随机数
        rand = time.time()
        # 获取当前时间
        date = datetime.datetime.now().strftime('%Y%m%d%H%M%S{}').format(int(rand))

        # 保存数据至数据库

        # 事务装饰器
        sid = transaction.savepoint()

        # 订单地址
        site = "{}{}{}-{}".format(sites.hcity, sites.hproper, sites.harea, sites.detail_address)
        total_price = 0
        for sku in sku_id:
            sku = int(sku)
            # 获取sku
            goods_sku = Goods_SKU.objects.get(pk=sku, is_delete=False)
            # 获取商品数量
            count = int(r.hget(user, sku))
            # 商品总价
            total_price += goods_sku.goods_price * count
        # 实付金额
        price_sum = transport.carriage_price + total_price

        order = OrderStatus.objects.create(
            order_number=date,  # 订单编号
            order_money=total_price,  # 商品总价
            userID=user_id,  # 用户ID
            address_name=sites.take_user,  # 收货人姓名
            address_tel=sites.tel_sign,  # 收货人电话
            address_site=site,  # 收货地址
            order_state=0,  # 订单状态
            transport=ModeTransport.objects.get(pk=transport_mode),  # 运输方式
            payment_method=PaymentMethod.objects.get(pk=1),  # 支付方式
            actually_paid=price_sum,  # 订单总价
            address_note=remark,  # 备注
        )

        for sku in sku_id:
            sku = int(sku)
            # 获取sku
            goods_sku = Goods_SKU.objects.get(pk=sku, is_delete=False)
            # 获取商品数量
            count = int(r.hget(str(user), str(sku)))
            try:
                #     商品订单表
                OrderCommodity.objects.create(
                    oderId_id=order.pk,  # 订单ID
                    skuID_id=goods_sku.pk,  # 商品ID
                    goods_count=count,  # 商品数量
                    goods_price=goods_sku.goods_price  # 商品价格
                )
            except OrderStatus.DoesNotExist:
                # 回滚事务
                transaction.savepoint_rollback(sid)
                return JsonResponse({"star": 5, "error": "保存数据库失败"})
            # 订单成功时,从商品列表中减去商品数量
            try:
                for sku in sku_id:
                    count = int(r.hget(user, sku))
                    goods_sku = Goods_SKU.objects.get(pk=sku, is_delete=False)
                    goods_sku.repertory -= count
                    goods_sku.save()
            except:
                # 回滚事务
                transaction.savepoint_rollback(sid)
                return JsonResponse({"star": 6, "error": "更新商品数量失败"})

            # 订单成功时,销量增加
            try:
                for sku in sku_id:
                    count = int(r.hget(user, sku))
                    goods_sku = Goods_SKU.objects.get(pk=sku, is_delete=False)
                    goods_sku.sales += count
                    goods_sku.save()
            except:
                # 回滚事务
                transaction.savepoint_rollback(sid)
                return JsonResponse({"star": 7, "error": "更新商品销量失败"})
        # 删除Redis中的数据
        try:
            for sku in sku_id:
                r.hdel(user, sku)
        except:
            return JsonResponse({"star": 8, "error": "redis数据库删除失败"})
        # 提交事务
        order.save()
        transaction.savepoint_commit(sid)
        # 全部执行成功时.跳转至确实支付页面(快照完成)
        return JsonResponse({"star": 200, "error": "提交订单成功", "order_id": date})
    else:
        return JsonResponse({"star": 500, "error": "请求方式错误"})


# 确认支付
@Session
def pay(request):
    if request.method == "GET":
        # 获取用户id
        sku_ids = request.GET.get('id')
        user_id = Members.objects.get(user_ID=request.session.get('id'))
        # 查询商品数据
        sks = OrderStatus.objects.get(userID=user_id.pk, is_delete=False, order_number=sku_ids)
        # 支付方式
        payment = PaymentMethod.objects.all()

        # 渲染页面
        context = {'orders': sks, "payment": payment}
        return render(request, 'pay.html', context)
    else:
        # post方式    确认支付
        oderId_id = str(request.POST.get('oderId_id'))  # 获取订单编号
        # 获取当前用户ID
        user_id = request.session.get('id')
        # 获取订单金额
        try:
            order = OrderStatus.objects.get(order_number=oderId_id, userID=Members.objects.get(user_ID=user_id).pk)
        except:
            return JsonResponse({"star": 400})
        #     读取私钥
        app_private_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/private.txt')).read()
        # 读取公钥
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/public.txt')).read()

        alipay = AliPay(
            appid="2016092300576093",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_wap_pay(
            out_trade_no=oderId_id,
            # 订单金额
            total_amount=str(order.order_money),
            subject="订单描述:双十一大促销",
            # 支付成功时跳转的页面
            return_url='http://127.0.0.1:8000/order/pay_star',
            notify_url=None  # 可选, 不填则使用默认notify url
        )

        res = 'https://openapi.alipaydev.com/gateway.do?{}'.format(order_string)
        return JsonResponse({"star": 200, "res": res})


# 订单查询验证状态
@Session
def star(request):
    #     读取私钥
    app_private_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/private.txt')).read()
    # 读取公钥
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/public.txt')).read()

    alipay = AliPay(
        appid="2016092300576093",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    # 获取参数
    out_trade_no = request.GET.get('out_trade_no')
    paid = False
    for i in range(3):
        result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            paid = True
            break
        else:
            time.sleep(10)
    #  判断是否支付成功
    if paid is False:
        context = {'star': '支付失败!'}
    else:
        context = {'star': '支付成功!'}
    #     修改订单状态
    trade_no = request.GET.get('trade_no')
    order = OrderStatus.objects.filter(order_number=trade_no, is_delete=False).update(order_state=5)
    # 渲染页面
    return render(request, 'pay_detail.html', context)


# 全部订单
@Session
def order_all(request):
    # 获取当前用户id
    user_id = Members.objects.get(user_ID=request.session.get('id')).pk
    # 获取订单
    order = OrderStatus.objects.filter(userID=user_id).order_by('-create_date')
    context = {"order":order}
    return render(request, 'all_order.html',context)
