from django import forms
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

#   用户注册验证
from user.models import Addreses


class UserReg(forms.Form):
    user_id = forms.CharField(error_messages={'required':'正确填写号码!'},min_length=11,max_length=11,required=True,
                              validators=[RegexValidator(r'^1[3-9]\d{9}$', '号码格式不正确')])
    password= forms.CharField(error_messages={'min_length':'密码最少6位','required':'密码必填!'},min_length=6,required=True)
    re_password = forms.CharField(error_messages={'required':'不可为空!'})
    yzm = forms.CharField(error_messages={'required':'验证码必填!'})
    def clean_re_password(self):
        """
        第二次输入的密码验证
        :return:
        """
        pws1 = self.cleaned_data.get('password')
        pws2 = self.cleaned_data.get('re_password')
        if pws1 and pws2 and(pws1 != pws2):
            raise forms.ValidationError("两次密码不一致")
        else:
            return pws2

    def clean_yzm(self):
        """
        验证码的获取
        :return:
        """
        yzm = self.cleaned_data.get('yzm')      # 表单验证码
        # yzm = forms.CharField(error_messages={'required': '验证码必填!','max_length':'最多四位','min_length':'填写错误'},max_length=4,min_length=4)

        con = get_redis_connection()
        re_yzm = con.get('yzm')        # 获取缓存验证码
        re_yzm = re_yzm.decode('utf-8')
        # try:
        if yzm != re_yzm:
            raise forms.ValidationError('验证码错误或失效!')
        else:
            return self.cleaned_data.get('yzm')
        # except:
        #     return forms.ValidationError('验证码错误!')


#  会员收货地址验证
class AddressForm(forms.ModelForm):
    tel_sign = forms.CharField(error_messages={'required': '正确填写号码!'}, min_length=11, max_length=11, required=True,
                               validators=[RegexValidator(r'^1[3-9]\d{9}$', '号码格式不正确')])

    class Meta:
        model = Addreses         # 对应数据模型
        fields = ['take_user','detail_address','is_default','harea','hcity','hproper']

        # 判断是否为空
        error_messages={
            'take_user': {'required':'收件人不能为空!'},
            'detail_address':{'required':'详细地址必填!'},
            'hcity':{'required':'必填项!'}, #   省
            'hproper':{'required':'必填项!'},#   市
            'harea':{'required':'必填项!'},#   区


        }



