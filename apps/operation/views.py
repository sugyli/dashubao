import json
import datetime

#from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.shortcuts import reverse

from operation import forms as operation_forms
from users import forms as users_forms
from operation import models as operation_models
#from users import models as users_models
from utils import modelhelp


class AddUserZan(View):
    """
    用户添加赞
    """

    def post(self, request):

        if not request.user.is_authenticated:
            # 判断用户登录状态
            response = HttpResponse('{"status":"fail","msg":"还没有登录"}', content_type='application/json')
            return modelhelp.del_auth_response(response)


        bookid = request.POST.get('bookid', '')
        bookid = bookid.strip()
        novel = modelhelp.get_one_book({'url_md5': bookid})
        if not novel:
            response = HttpResponse('{"status":"fail","msg":"这本书不存在"}', content_type='application/json')
            return modelhelp.add_auth_response(response)
        user = request.user
        piao = user.get_piao_count()

        today = datetime.date.today()

        yiyongpiao = operation_models.UserZan.objects.filter(user=user,create_time=today).count()

        if yiyongpiao >= piao:
            response = HttpResponse('{"status":"success","msg":"您今天的推荐票已经用完"}', content_type='application/json')
            return modelhelp.add_auth_response(response)
        uz_obj = operation_models.UserZan()
        uz_obj.user = user
        uz_obj.novel = novel
        uz_obj.save()
        novel.novel_zan_nums += 1
        novel.save()
        user.score += 1
        user.save()
        shen = piao - (yiyongpiao+1)

        response = HttpResponse('{"status":"success","msg":"投票成功获得1积分剩余%s票"}'%(shen), content_type='application/json')
        return modelhelp.add_auth_response(response)



class AddUserFav(View):
    """
    用户收藏，用户取消收藏
    """

    def post(self, request):
        if not request.user.is_authenticated:
            # 判断用户登录状态
            response = HttpResponse('{"status":"fail","msg":"还没有登录"}', content_type='application/json')
            return modelhelp.del_auth_response(response)
        userfav_form = operation_forms.AddUserFavForm(request.POST)
        if userfav_form.is_valid():
            bookid = request.POST.get('bookid', '')
            chapterid = request.POST.get('chapterid', '')
            bookid = bookid.strip()
            chapterid = chapterid.strip()
            novel = modelhelp.get_one_book({'url_md5': bookid})
            exist_records = operation_models.NovelFavorite.objects.filter(user=request.user, novel=novel).first()
            if exist_records:
                # 如果记录已经存在， 则表示用户取消收藏
                if exist_records.chapterid == chapterid:
                    exist_records.delete()
                    novel.novel_fav_nums -= 1
                    if novel.novel_fav_nums < 0:
                        novel.novel_fav_nums = 0
                    novel.save()
                    response = HttpResponse('{"status":"success","msg":"删除书签成功"}', content_type='application/json')
                    return modelhelp.add_auth_response(response)
                else:
                    exist_records.chapterid = chapterid
                    exist_records.save()
                    response = HttpResponse('{"status":"success","msg":"修改书签成功"}', content_type='application/json')
                    return modelhelp.add_auth_response(response)
            elif novel:
                user_fav = operation_models.NovelFavorite()
                user_fav.user = request.user
                user_fav.novel = novel
                user_fav.chapterid = chapterid
                user_fav.save()
                novel.novel_fav_nums += 1
                novel.save()
                response = HttpResponse('{"status":"success","msg":"添加书签成功"}', content_type='application/json')
                return modelhelp.add_auth_response(response)
            else:
                response = HttpResponse('{"status":"fail","msg":"提交失败"}', content_type='application/json')
                return modelhelp.add_auth_response(response)
        else:
            response = HttpResponse(json.dumps(userfav_form.errors), content_type='application/json')
            return modelhelp.add_auth_response(response)


class UserUpdatePwd(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        if not request.user.is_authenticated:
            #判断用户登录状态
            response = HttpResponse('{"status":"fail","msg":"还没有登录"}', content_type='application/json')
            return modelhelp.del_auth_response(response)
        modify_form = users_forms.ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd1 = pwd1.strip()
            pwd2 = request.POST.get("password2", "")
            pwd2 = pwd2.strip()
            if pwd1 != pwd2:
                response = HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
                return modelhelp.add_auth_response(response)
            user = request.user
            if user.is_superuser > 0:
                response = HttpResponse('{"status":"fail","msg":"此账户只能在后台修改密码"}', content_type='application/json')
                return modelhelp.add_auth_response(response)
            user.password = make_password(pwd2)
            user.old_password = ''
            user.save()

            response = HttpResponse('{"status":"success","msg":"密码修改成功"}', content_type='application/json')
            return modelhelp.add_auth_response(response)
        else:
            response = HttpResponse(json.dumps(modify_form.errors), content_type='application/json')
            return modelhelp.add_auth_response(response)



class IsLogin(View):
    '''

    ajax 验证登录
    '''

    def post(self, request):
        if not request.user.is_authenticated:
            login_form = users_forms.LoginForm(request.POST)
            if login_form.is_valid():
                user_name = request.POST.get("username", "")
                pass_word = request.POST.get("password", "")
                user_name = user_name.strip()
                pass_word = pass_word.strip()
                user = modelhelp.authenticate(username=user_name, password=pass_word)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        user = json.dumps(modelhelp.ajaxuser(user))
                        response = HttpResponse('{"status":"success","msg":"登录成功","data":%s}' % user,
                                                content_type='application/json')
                        return modelhelp.add_auth_response(response)
                    else:

                        response = HttpResponse('{"status":"fail","msg":"账户未激活"}', content_type='application/json')

                else:
                    response = HttpResponse('{"status":"fail","msg":"用户名或密码错误"}', content_type='application/json')

            else:

                response = HttpResponse(json.dumps(login_form.errors), content_type='application/json')


            return modelhelp.del_auth_response(response)

        user = json.dumps(modelhelp.ajaxuser(request.user))
        response = HttpResponse('{"status":"success","msg":"用户是登录状态","data":%s}'%user, content_type='application/json')
        return modelhelp.add_auth_response(response)


class IsReadBookshelf(View):
    '''
    书架记录
    '''

    def get(self, request,bookid, chapterid):
        if request.user.is_authenticated:
            novelfavorite = operation_models.NovelFavorite.objects.filter(user=request.user, novel=bookid, chapterid=chapterid).first()

            if novelfavorite:
                novelfavorite.update_time = datetime.datetime.now()
                novelfavorite.save()


        return HttpResponseRedirect(reverse('novels:novels_content', args=[chapterid]))



