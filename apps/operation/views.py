import base64
import urllib.parse

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect

from operation import forms as operation_forms
from operation import models as operation_models
from utils import modelhelp
from utils import help
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.

temp_dir_m = 'dashubao/m/'
temp_dir_p = 'dashubao/p/'
temp_dir_w = 'dashubao/w/'
def get_temp(s, temp_dir=temp_dir_m):
    return "{0}{1}".format(temp_dir, s)
class AddUserAsk(LoginRequiredMixin,View):
    """
    用户添加咨询
    """

    def get(self, request,comefrom):
        comefrom = help.decrypt_urllib_base64(comefrom)
        return render(request, get_temp("shuku-userask.html"),{
            'comefrom': comefrom
        })

    def post(self, request,comefrom):

        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"还没有登录"}', content_type='application/json')

        userask_form = operation_forms.UserAskForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit=False)
            # commit=False告诉Django先不提交到数据库.
            userask.user = request.user  # 添加额外数据
            userask.comefrom = help.decrypt_urllib_base64(comefrom)  # 添加额外数据
            userask.save()  # 发送到数据库
            return HttpResponse('{"status":"success","msg":"提交成功"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(userask_form.errors), content_type='application/json')


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
            exist_records = operation_models.NovelFavorite.objects.filter(user=request.user, novel=novel)
            if exist_records:
                # 如果记录已经存在， 则表示用户取消收藏
                exist_records.delete()
                novel.novel_fav_nums -= 1
                if novel.novel_fav_nums < 0:
                    novel.novel_fav_nums = 0
                novel.save()
                return HttpResponse('{"status":"success","msg":"删除书签成功"}', content_type='application/json')
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










        bookid = request.POST.get('bookid', '')
        chapterid = request.POST.get('chapterid', '')

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id),
                                                    fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

