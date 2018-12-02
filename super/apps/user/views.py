import random
import uuid

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django_redis import get_redis_connection

from db.login_session import Session
# from user.base_view import send_sms
from user.base_view import send_sms

from user.forms import UserReg, AddressForm
from user.models import Members, Addreses
import hashlib

"""
用户(User)模块中心,功能: 会员新增,会员退出登录,会员登录,会员资料修改,找回密码,会员中心
"""


#  会员页面
@Session
def member(request):
    user_id = request.session.get('id')
    data = Members.objects.get(user_ID=user_id)
    context = {'db_data': data}
    return render(request, 'member.html', context)


#  会员注册
def reg(request):
    if request.method == 'POST':
        data = request.POST
        form = UserReg(data)
        if form.is_valid():  # 验证是否合法
            data = form.cleaned_data  # 清洗后的数据
            #     写入数据库
            ha = hashlib.md5(data.get('password').encode('utf-8'))
            pws = ha.hexdigest()  # 得到加密后的字符串
            try:
                Members.objects.create(user_ID=data.get('user_id'), password=pws)  # 存入数据库(持久性)
            except:
                context = {'errors': {'user_id': ['手机号已被注册!'], 'phone': data.get('user_id')}}  # 提示手机号已被注册,并回显号码
                return render(request, 'reg.html', context)
            return redirect('user:login')
        else:
            context = {'errors': form.errors, 'phone': data.get('user_id')}
            return render(request, 'reg.html', context)
    else:
        return render(request, 'reg.html')


# 会员登录
def login(request):
    if request.method == 'POST':
        data = request.POST
        ha = hashlib.md5(data.get('password').encode('utf-8'))  # 对输入的密码进行md5加密
        password = ha.hexdigest()  # 得到加密后的字符串
        try:
            num = Members.objects.get(user_ID=data.get('user_id'), password=password)  # 查询一条
        except:
            num = 0  # 如果没查询出结果,就为False
        if num:
            request.session['id'] = data.get('user_id')
            request.session['paw'] = password  # 设置登录session
            request.session.set_expiry(1800)  # 有效期为半小时
            # request.session.set_expiry(0)  # 关闭浏览器失效
            skip = request.GET.get('next')  # 检测是否是跳转登陆
            if skip:
                return redirect(skip)  # 回跳
            else:
                return redirect('user:member')  # 登录成功,跳转至个人中心页面
        else:
            context = {'data': {'user_id': data.get('user_id')}}
            return render(request, 'login.html', context)
    else:

        return render(request, 'login.html')


#  找回密码
class ForgetPassword(View):
    def get(self, request):
        return render(request, 'forgetpassword.html')

    #   post提交
    def post(self, request):
        data = request.POST
        form = UserReg(data)
        if form.is_valid():
            data = form.cleaned_data  # 得到清洗后的数据
            ha = hashlib.md5(data.get('password').encode('utf-8'))
            # 对密码进行md5加密处理
            password = ha.hexdigest()
            if data.get('yzm'):  # 验证码输入正确(假定)
                res = Members.objects.filter(user_ID=data.get('user_id')).update(password=password)
                # 修改密码
                if res:
                    return redirect('user:login')  # 修改成功,跳转值登录页面
                else:
                    content = {'result': '失败!用户不存在'}
                    return redirect('user:ForgetPassword', content)
            else:
                content = {'result': '验证码错误!'}
                return redirect('user:ForgetPassword', content)
        else:
            content = {'errors': form.errors}
            return render(request, 'forgetpassword.html', content)


#   个人资料
def infor(request):
    # 显示页面数据,供给用户修改及查看
    user_id = request.session.get('id')
    # 从session中获取响应数据
    password = request.session.get('paw')
    if request.method == 'POST':
        data = request.POST
        head_portrait = request.FILES.get('head_portrait')  # 头像
        nick_name = data.get('nick_name')  # 昵称
        user_sex = data.get('user_sex')  # 性别
        borm_date = data.get('borm_date')  # 生日
        school = data.get('school')  # 学校
        address = data.get('address')  # 详细地址
        hometown = data.get('hometown')  # 故乡
        user_ID = data.get('user_ID')  # 电话
        Members.objects.filter(user_ID=user_id, password=password).update(
            nick_name=nick_name,
            user_sex=user_sex,  # 更新个人资料(更新数据)
            borm_date=borm_date,
            school=school, address=address,
            hometown=hometown,
            user_ID=user_ID
        )

        #  更新数据
        mem = Members.objects.get(user_ID=user_id)
        mem.head_portrait = head_portrait  # 注意: 添加文件只能使用对象的方法添加
        mem.save()  # 保存数据

        return redirect('user:member')
    else:

        if all([user_id, password]):  # 判断是否登陆,已登陆为True,否则为False
            try:
                data = Members.objects.get(user_ID=user_id, password=password)  # 查询一条记录
            except:
                return redirect('user:login')
            context = {'data': data}  # 响应数据到模板
            return render(request, 'infor.html', context)
        else:
            return redirect('user:login')


#  安全退出
def Quit(request):
    request.session.clear()
    return redirect('user:login')


# 积分
@Session
def integral(request):
    user_id = request.session.get('id')
    data = Members.objects.get(user_ID=user_id)
    context = {'db_data': data}
    return render(request, 'integral.html', context)


# 积分兑换
@Session
def cash(request):
    user_id = request.session.get('id')
    data = Members.objects.get(user_ID=user_id)
    context = {'db_data': data}
    return render(request, 'integralexchange.html', context)


# 待付款
def obligation(request):
    return render(request, 'allorder.html')


#  收货地址管理
class Gladdress(View):
    # 判断是否登陆
    def get(self, request):
        # 回显数据
        try:
            id = Members.objects.get(user_ID=request.session.get('id')).pk  # 获取当前用户的id
            add = Addreses.objects.filter(add_user=id, is_delete=False).order_by('-is_default')  # 地址对象
            context = {'add': add}
            return render(request, 'gladdress.html', context)
        except:
            return redirect('user:login')

    def post(self, request):
        return HttpResponse('请求方式错误')


# 地址添加页
class Address(View):

    def get(self, request):
        return render(request, 'address.html')

    def post(self, request):
        if request.session.get('id'):
            id = Members.objects.get(user_ID=request.session.get('id')).pk  # 获取用户id
            data = request.POST
            form = AddressForm(data)  # 清洗数据
            if form.is_valid():
                cleaned_data = form.cleaned_data  # 得到清洗成功的后的数据
                # 检测用户收货地址是否超过六条
                if Addreses.objects.filter(add_user=id).count() < 6:
                    # 将地址添加进数据库,持久保存
                    if cleaned_data.get('is_default'):
                        # 如果设置为默认,就将全部的设置为False
                        Members.objects.get(pk=id).addreses_set.filter(is_delete=False).update(is_default=False)
                        # 重新设置当前的地址为默认的
                        Members.objects.get(pk=id).addreses_set.create(**cleaned_data)
                    else:
                        # 如果不是默认的,就直接保存
                        Members.objects.get(pk=id).addreses_set.create(**cleaned_data)
                else:
                    context = {'error': '单个用户地址数不能大于6'}
                    return render(request, 'address.html', context)
                return redirect('user:gladdress')
            else:
                context = {'errors': form.errors, 'data': data}
                return render(request, 'address.html', context)
        else:
            return redirect('user:login')


# 修改地址
@Session
def address_edit(request):
    if request.method == 'GET':
        # 接收参数
        id = request.GET.get('id')
        # 获得地址
        content = Addreses.objects.get(pk=id)
        # 准备渲染数据
        context = {'edit': content}
        return render(request, 'address_edit.html', context)
    # post修改请求
    else:
        data = request.POST  # 修改数据  # 获取数据
        # 获取ID
        try:
            id = data.get('id')
        except:  # 检测防止非法用户篡改ID值
            return redirect('user:gladdress')
        # 使用form表单验证数据
        form = AddressForm(data)
        if form.is_valid():  # 清洗数据为True时
            #             得到清洗后的数据
            cleaned_data = form.cleaned_data
            Addreses.objects.filter(pk=id).update(**cleaned_data)  # 更新数据
            return redirect('user:gladdress')  # 更新成功后跳转至列表页
        else:
            # 清洗失败时,返回错误,并回显
            content = Addreses.objects.get(pk=id)
            context = {'errors': form.errors, 'edit': content}
            return render(request, 'address_edit.html', context)



#

# 删除地址
@Session
def address_del(request):
    if request.method=="POST":
            # 接收参数
        try:
            id = request.POST.get('id')
        except:
            return JsonResponse({'stat':1,'hint':'参数错误!'})
        try:
            Addreses.objects.filter(pk = id).update(is_delete = True)
            return JsonResponse({'stat':200,'hint':'删除成功!'})
        except:
            return JsonResponse({'stat':2,'hint':'删除失败!'})
    else:
        return JsonResponse({'stat':0,'hint':'请求方式错误!'})


# 修改默认地址
@Session
def default_edit(request):
            #判断请求方式
    if request.method == "POST":
        # 修改        接收参数
        try:
            id = request.POST.get('id')     # 获取地址id
            user = Members.objects.get(user_ID=request.session.get('id')).pk        # 获得用户ID
        except:
            return JsonResponse({"stat":0,"hint":"参数错误!"})
        try:
            Addreses.objects.filter(add_user=user).update(is_default=False)   #   全部为False
            Addreses.objects.filter(add_user=user, pk=id).update(is_default=True)  # 设置为False
            return JsonResponse({"stat": 200, "hint": "修改成功!"})
        except:
            return JsonResponse({"stat":1,"hint":"修改错误!"})

    else:
        return JsonResponse({"stat":400,"hint":"请求方式错误!"})





# 发送验证码
def verification(request):
    if request.method =="POST":
        # 获取用户输入的手机号
        tel = request.POST.get('user_id')
        re = [str(random.randint(0, 9)) for _ in range(4)]
        res = ''.join(re)  # 获得4位随机码
        # print(res)  # 测试打印验证码
        con = get_redis_connection("default")
        result = con.set('yzm', res)  # 将验证码写入redis缓存
        if (result):
            con.expire('yzm', 60)
            # 发送短信验证码
            __business_id = uuid.uuid1()
            params = "{\"code\":\"%s\",\"product\":\"SMS_151991471\"}" % res
            send_sms(__business_id, tel, "深度资源", "SMS_151991471", params).decode('utf-8')
            # 响应ajax
            return JsonResponse({'state': 200})
    else:
        return JsonResponse({'state': 400})