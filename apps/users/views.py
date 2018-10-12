import datetime
import math
import json

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import login, logout
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from users import forms as users_forms
from users import models as users_models
from operation import models as operation_models
from utils import help,modelhelp
from utils.mixin_utils import LoginRequiredMixin
from utils.email_send import send_register_email



temp_dir_m = 'dashubao/m/'
temp_dir_p = 'dashubao/p/'
temp_dir_w = 'dashubao/w/'


def get_temp(s, temp_dir=temp_dir_m):
    return "{0}{1}".format(temp_dir, s)


dt_s = datetime.datetime.now().date()
dt_e = (dt_s - datetime.timedelta(7))  # 2018-7-08


class LogoutView(View):
    """
    用户登出
    """

    def get(self, request):
        logout(request)
        next_to = request.GET.get('next', '')
        url = '/'
        if next_to:
            url = next_to
        response = HttpResponseRedirect(url)
        return modelhelp.del_auth_response(response)


class LoginView(View):
    """
    用户登录
    """
    def get(self, request):
        #logout(request)
        next_to = request.GET.get('next', '')
        response = render(request, get_temp('login.html', temp_dir_p), {
            'next_to': next_to
        })
        return response

    def post(self, request):

        login_form = users_forms.LoginForm(request.POST)
        next_to = request.POST.get('next_to', '')
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user_name = user_name.strip()
            pass_word = pass_word.strip()
            user = modelhelp.authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if next_to:
                        response = HttpResponseRedirect(next_to)
                    else:
                        response = HttpResponseRedirect(
                            reverse("users:users_home"))
                    return modelhelp.add_auth_response(response)
                else:
                    return render(
                        request, get_temp(
                            'login.html', temp_dir_p), {
                            "msg": "用户未激活！", "next_to": next_to})
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
    """
    用户注册
    """

    def get(self, request):
        return render(request, get_temp('register.html', temp_dir_p))

    def post(self, request):
        register_form = users_forms.RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            user_name = user_name.strip()
            # 没有返回【】
            if modelhelp.authuser(user_name):
                return render(request, get_temp('register.html', temp_dir_p), {
                              "register_form": register_form, "msg": "账户已经存在"})
            pass_word = request.POST.get("password", "")
            pass_word = pass_word.strip()
            user_profile = users_models.UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = True
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息
            user_message = users_models.UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎%s注册本站,本站样式在后期会慢慢完善, 前期大量的工作在数据"%user_profile.username
            user_message.save()

            #send_register_email(user_name, "register")
            return render(
                request, get_temp("login.html", temp_dir_p), {
                    "msg": "注册成功,请登录",
                    "register_name": user_name
                })
        else:
            return render(
                request, get_temp('register.html', temp_dir_p), {
                    "register_form": register_form})


class ForgetPwdView(View):
    '''
       忘记密码发送邮件
    '''

    def get(self, request):
        return render(request, get_temp('forgetpwd.html', temp_dir_p))

    def post(self, request):
        forget_form = users_forms.ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            email = email.strip()
            if not modelhelp.authuser(email):
                return render(
                    request, get_temp(
                        'email_msg.html', temp_dir_p), {
                        'msg': '邮箱不存在'})
            send_register_email(email, "forget")
            return render(
                request, get_temp(
                    'email_msg.html', temp_dir_p), {
                    'msg': '邮件已经发送 ,请到邮箱查看'})
        else:
            return render(
                request, get_temp('forgetpwd.html', temp_dir_p), {
                    "forget_form": forget_form})


class ResetView(View):
    '''
    重置密码页面
    '''

    def get(self, request, active_code):
        kwargs = {
            'code': active_code,
            'is_used': 0,
        }
        all_records = users_models.EmailVerifyRecord.objects.filter(
            send_time__gt=dt_e, **kwargs)
        if all_records:
            return render(
                request, get_temp('password_reset.html', temp_dir_p), {
                    'active_code': active_code})
        else:
            return render(
                request, get_temp(
                    'email_msg.html', temp_dir_p), {
                    'msg': '验证码失效，请从新获取'})

        # return render(request, get_temp('login.html'))


class ModifyPwdView(View):
    '''

    重置密码页面 POST 因为展现需要 CODE 所以单独写个
    '''

    def post(self, request):
        modify_form = users_forms.ModifyPwdForm(request.POST)
        active_code = request.POST.get("active_code", "")
        active_code = active_code.strip()
        if modify_form.is_valid() and active_code:
            pwd1 = request.POST.get("password1", "")
            pwd1 = pwd1.strip()
            pwd2 = request.POST.get("password2", "")
            pwd2 = pwd2.strip()
            if pwd1 != pwd2:
                return render(
                    request, get_temp('password_reset.html', temp_dir_p), {
                        "active_code": active_code, "msg": "密码不一致"})
            kwargs = {
                'code': active_code,
                'is_used': 0
            }
            record = users_models.EmailVerifyRecord.objects.filter(
                send_time__gt=dt_e, **kwargs).first()

            if record:
                params = {
                    'email': record.email,
                    'is_superuser': 0
                }
                user = users_models.UserProfile.objects.filter(
                    **params).first()
                if user:
                    user.password = make_password(pwd2)
                    user.old_password = ''
                    user.save()

                    record.is_used = 1
                    record.save()
                    return render(
                        request, get_temp(
                            'login.html', temp_dir_p), {
                                'msg': '密码修改成功,请登录'})
                else:
                    msg = '用户不存在或超级用户不给修改'
            else:
                msg = '验证码失效'

            return render(
                request, get_temp('password_reset.html', temp_dir_p), {
                    "active_code": active_code, "msg": msg})
        else:
            return render(
                request, get_temp('password_reset.html', temp_dir_p), {
                    "active_code": active_code, "modify_form": modify_form})


class M_QandaoView(LoginRequiredMixin, View):
    '''
    用户签到
    '''

    def get(self, request):
        user = request.user
        qiandaoobj = user.userqiandao_set.all().order_by('qiandao_time')
        from django.conf import settings
        qiandaodate = settings.USER_QIANDAO
        if qiandaoobj:
            oneobj = qiandaoobj.last()
            qiandaotime = oneobj.qiandao_time

            today = datetime.date.today()
            # 昨天时间
            yesterday = today - datetime.timedelta(days=1)

            #today = datetime.datetime.strptime(str(today), '%Y-%m-%d')
            yesterday = datetime.datetime.strptime(str(yesterday), '%Y-%m-%d')

            delta = qiandaotime - yesterday

            c = qiandaoobj.count()
            if delta.days == 1:  # 今天已经签到过了
                frequency = c
                if frequency == 30:
                    todayjifen = "签到成功，获%d积分" % qiandaodate[5][4]['f']
                    nextjifen = '将从新开启'
                else:
                    a = math.ceil(frequency / 5) - 1
                    b = frequency % 5 - 1
                    todayjifen = "签到成功，获%d积分" % qiandaodate[a][b]['f']
                    c = math.ceil((frequency + 1) / 5) - 1
                    d = (frequency + 1) % 5 - 1
                    nextjifen = "明日签到，可获得%d积分" % qiandaodate[c][d]['f']
            elif delta.days == 0 and c < 30:  # 昨天签到的
                qiandaoobj = users_models.UserQiandao()
                qiandaoobj.user = user
                qiandaoobj.save()
                frequency = c + 1
                a = math.ceil(frequency / 5) - 1
                b = frequency % 5 - 1
                user.score += qiandaodate[a][b]['f']
                user.save()
                c = math.ceil((frequency + 1) / 5) - 1
                d = (frequency + 1) % 5 - 1
                todayjifen = "签到成功，获%d积分" % qiandaodate[a][b]['f']
                nextjifen = "明日签到，可获得%d积分" % qiandaodate[c][d]['f']

            else:
                qiandaoobj.delete()
                qiandaoobj1 = users_models.UserQiandao()
                qiandaoobj1.user = user
                qiandaoobj1.save()
                frequency = 1
                user.score += qiandaodate[0][0]['f']
                user.save()
                todayjifen = "签到成功，获%d积分" % qiandaodate[0][0]['f']
                nextjifen = "明日签到，可获得%d积分" % qiandaodate[0][1]['f']

        else:
            qiandaoobj = users_models.UserQiandao()
            qiandaoobj.user = user
            qiandaoobj.save()
            frequency = 1
            user.score += qiandaodate[0][0]['f']
            user.save()
            todayjifen = "签到成功，获%d积分" % qiandaodate[0][0]['f']
            nextjifen = "明日签到，可获得%d积分" % qiandaodate[0][1]['f']

        return render(request, get_temp('usercenter-qiandao.html'), {
            'frequency': frequency,
            'qiandaodate': qiandaodate,
            'todayjifen': todayjifen,
            'nextjifen': nextjifen

        })


class M_UserindexView(LoginRequiredMixin, View):
    '''
    用户首页
    '''

    def get(self, request):
        comefrom = help.encryption_urllib_base64(request.path)

        return render(request, get_temp('usercenter-index.html'),{
            'comefrom': comefrom
        })


class M_UserinfoView(LoginRequiredMixin, View):
    """
    用户信息
    """
    def get(self, request):
        return render(request, get_temp('usercenter-info.html'))

    def post(self, request):
        userinfo_form = users_forms.M_UserInfoForm(
            request.POST, instance=request.user)
        if userinfo_form.is_valid():
            email = request.POST.get("email", "")
            email = email.strip()

            if users_models.UserProfile.objects.filter(~Q(id = request.user.id),username = email):
                return HttpResponse('{"status":"fail","msg":"邮箱已经存在"}', content_type='application/json')

            userinfo_form.save()
            return HttpResponse(
                '{"status":"success","msg":"保存成功"}',
                content_type='application/json')
        else:
            return HttpResponse(
                json.dumps(
                    userinfo_form.errors),
                content_type='application/json')


class M_UpdatePwdView(LoginRequiredMixin, View):

    """
    修改密码界面
    """

    def get(self, request):

        return render(request, get_temp('usercenter-pwd.html'))


class M_MessageView(LoginRequiredMixin, View):

    '''
    我的消息
    '''

    def get(self, request):
        all_messages = users_models.UserMessage.objects.filter(
            user=request.user.id).order_by("-create_time")
        # 用户进入个人消息后清空未读消息的记录
        all_unread_messages = all_messages.filter(has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5)

        messages = p.page(page)

        return render(request, get_temp('usercenter-message.html'), {
            'messages': messages
        })



class M_GonggaoView(LoginRequiredMixin, View):

    '''
    公告
    '''

    def get(self, request):
        all_messages = users_models.UserMessage.objects.filter(
            user=0).order_by("-create_time")
        # 用户进入个人消息后清空未读消息的记录
        all_unread_messages = all_messages.filter(has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5)

        messages = p.page(page)

        return render(request, get_temp('usercenter-gonggao.html'), {
            'messages': messages
        })



class M_AskView(LoginRequiredMixin, View):
    """
    我的咨询
    """
    def get(self, request):

        all_messages = users_models.UserAsk.objects.filter(user=request.user).order_by("-create_time")

        #对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5)

        messages = p.page(page)
        return render(request, get_temp('usercenter-ask.html'), {
            "messages":messages,
        })


class M_FavBookView(LoginRequiredMixin, View):
    """
    我收藏的书
    """
    def get(self, request):
        all_favbooks = operation_models.NovelFavorite.objects.filter(user=request.user).order_by('-novel__update_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_favbooks, 5)

        favbooks = p.page(page)

        return render(request, get_temp('usercenter-favbook.html'),{
            'favbooks': favbooks
        })


class M_AddUserAskView(LoginRequiredMixin, View):
    """
    用户添加咨询
    """

    def get(self, request, comefrom):
        comefrom = help.decrypt_urllib_base64(comefrom)
        return render(request, get_temp("shuku-userask.html"), {
            'comefrom': comefrom
        })

    def post(self, request, comefrom):

        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse(
                '{"status":"fail","msg":"还没有登录"}',
                content_type='application/json')

        userask_form = users_forms.UserAskForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit=False)
            # commit=False告诉Django先不提交到数据库.
            userask.user = request.user  # 添加额外数据
            userask.comefrom = help.decrypt_urllib_base64(comefrom)  # 添加额外数据
            userask.save()  # 发送到数据库
            return HttpResponse(
                '{"status":"success","msg":"提交成功"}',
                content_type='application/json')

        else:
            return HttpResponse(
                json.dumps(
                    userask_form.errors),
                content_type='application/json')


class M_TouxianView(View):

    def get(self, request):
        z = settings.USER_LEVEL

        return render(request, get_temp("usercenter-touxian.html"),{
            'z': z
        })
