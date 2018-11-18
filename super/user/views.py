from django.shortcuts import render

# 用户模块

#  会员页面
def member(request):
    return render(request,'member.html')
