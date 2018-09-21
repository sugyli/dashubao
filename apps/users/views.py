import logging

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login ,logout
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect

from users import forms as users_forms
from users import models as users_models
from utils import help

logger = logging.getLogger(__name__)

temp_dir_m = 'dashubao/m/'
temp_dir_p = 'dashubao/p/'
temp_dir_w = 'dashubao/w/'
def get_temp(s, temp_dir=temp_dir_m):
    return "{0}{1}".format(temp_dir, s)

class CustomBackend():

    def authenticate(self, username=None, password=None):
        try:
            user = users_models.UserProfile.objects.get(
                Q(username=username) | Q(email=username))

            if len(password) > 0 and (user.check_password(password)
                                      or user.old_password == help.get_md5(password)):
                return user

        except Exception as e:
            logger.debug(e)
            return None

class LoginView(View):
    """
    用户登录
    """
    def get(self, request):
        logout(request)
        next_to = request.GET.get('next', '')
        response = render(request, get_temp('login.html',temp_dir_p),{
            'next_to': next_to
        })
        response.set_cookie('is_login', '')
        return response

    def post(self, request):

        login_form = users_forms.LoginForm(request.POST)
        next_to = request.POST.get('next_to', '')
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user_name = user_name.strip()
            pass_word = pass_word.strip()
            custon_backend = CustomBackend()
            user = custon_backend.authenticate(username=user_name,password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if next_to:
                        response = HttpResponseRedirect(next_to)
                    else:
                        response = HttpResponseRedirect(reverse("users:users_home"))

                    response.set_cookie('is_login', 1)
                    return response
                else:
                    return render(request, get_temp('login.html',temp_dir_p),{
                        "msg": "用户未激活！",
                        "next_to": next_to
                    })
            else:
                return render(
                    request, get_temp('login.html', temp_dir_p), {
                        "msg": "用户名或密码错误！",
                        "next_to": next_to
                    })
        else:
            return render(
                request, get_temp('login.html', temp_dir_p), {
                    "login_form": login_form,
                    "next_to": next_to,

                })


class RegisterView(View):
    pass

class ForgetPwdView(View):
    pass






#m
class M_UserindexView(View):

    pass
