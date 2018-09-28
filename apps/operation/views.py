import json


from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password

from operation import forms as operation_forms
from users import forms as users_forms
from operation import models as operation_models
from users import models as users_models
from utils import modelhelp


class AddUserZan(View):
    """
    用户添加赞
    """

    def post(self, request):

        isview = request.POST.get('isview', '')
        bookid = request.POST.get('bookid', '')
        bookid = bookid.strip()
        isview = isview.strip()
        if isview:
            if request.user.is_authenticated and bookid:
                user = request.user
                novel = modelhelp.get_one_book({'url_md5':bookid})
                if novel and operation_models.UserZan.objects.filter(user=user, novel=novel):
                    response = HttpResponse('{"status":"success"}', content_type='application/json')
                    response.set_cookie('zan', 1)
                    return response
            response = HttpResponse('{"status":"fail"}', content_type='application/json')
            response.set_cookie('zan', 2)
            return response

        else:

            if not request.user.is_authenticated:
                # 判断用户登录状态
                response = HttpResponse('{"status":"fail","msg":"还没有登录"}', content_type='application/json')
                response.set_cookie('zan', 2)
                return response
            if bookid:
                user = request.user
                novel = modelhelp.get_one_book({'url_md5':bookid})
                if novel:
                    uz_obj = operation_models.UserZan.objects.filter(user=user, novel=novel)
                    if uz_obj:
                        uz_obj.delete()
                        novel.novel_zan_nums -= 1
                        if novel.novel_zan_nums < 0:
                            novel.novel_zan_nums = 0
                        novel.save()
                        response = HttpResponse('{"status":"success","msg":"已经取消赞"}', content_type='application/json')
                        response.set_cookie('zan', 2)
                        return response
                    else:
                        uz_obj = operation_models.UserZan()
                        uz_obj.user = user
                        uz_obj.novel = novel
                        uz_obj.save()
                        novel.novel_zan_nums += 1
                        novel.save()
                        response = HttpResponse('{"status":"success","msg":"谢谢点赞"}', content_type='application/json')
                        response.set_cookie('zan', 1)
                        return response

            response.set_cookie('zan', 2)
            return HttpResponse('{"status":"fail","msg":"提交失败"}', content_type='application/json')


class AddUserFav(View):
    """
    用户收藏，用户取消收藏
    """

    def post(self, request):
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"还没有登录"}', content_type='application/json')

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
                    return HttpResponse('{"status":"success","msg":"删除书签成功"}', content_type='application/json')
                else:
                    exist_records.chapterid = chapterid
                    exist_records.save()
                    return HttpResponse('{"status":"success","msg":"修改书签成功"}', content_type='application/json')

            elif novel:
                user_fav = operation_models.NovelFavorite()
                user_fav.user = request.user
                user_fav.novel = novel
                user_fav.chapterid = chapterid
                user_fav.save()
                novel.novel_fav_nums += 1
                novel.save()
                return HttpResponse('{"status":"success","msg":"添加书签成功"}', content_type='application/json')

            else:
                return HttpResponse('{"status":"fail","msg":"提交失败"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(userfav_form.errors), content_type='application/json')



class UserUpdatePwd(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        if not request.user.is_authenticated:
            #判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"还没有登录"}', content_type='application/json')

        modify_form = users_forms.ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd1 = pwd1.strip()
            pwd2 = request.POST.get("password2", "")
            pwd2 = pwd2.strip()
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            if user.is_superuser > 0:
                return HttpResponse('{"status":"fail","msg":"此账户只能在后台修改密码"}', content_type='application/json')
            user.password = make_password(pwd2)
            user.old_password = ''
            user.save()

            return HttpResponse('{"status":"success","msg":"密码修改成功"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

