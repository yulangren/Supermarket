
from django.shortcuts import redirect

# 检测会员登录的session    装饰器
def Session(old_function):          # 把调用装饰的视图函数传入
    def inner(request, *args, **kwargs):        # 传入参数
        if request.session.get('id'):           # 逻辑判断
            return old_function(request, *args, **kwargs)       # 返回视图函数
        else:
            return redirect('user:login')

    return inner        # 将装饰器返回
