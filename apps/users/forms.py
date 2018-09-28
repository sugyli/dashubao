import re

from django import forms

from users import models as users_models


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    #captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)
    #active_code = forms.CharField(required=True)


class M_UserInfoForm(forms.ModelForm):

    # def __init__(self, data=None, instance=None,uid=None):
    #     self.uid = uid
    #     super().__init__(
    #         data=data, instance=instance
    #     )
    class Meta:
        model = users_models.UserProfile
        fields = ['gender', 'mobile','email']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        if not mobile:
            raise forms.ValidationError(u"手机号码不能为空", code="mobile_invalid")

        REGEX_MOBILE = "^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")



class UserAskForm(forms.ModelForm):

    class Meta:
        model = users_models.UserAsk
        fields = ['message']


