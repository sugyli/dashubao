import logging
import math

from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
#from django.urls import reverse
from django.db.models import Q
from utils import modelhelp
from utils import help
from novels import models as novels_models
from users import models as users_models

logger = logging.getLogger(__name__)
temp_dir_m = 'dashubao/m/'
temp_dir_p = 'dashubao/p/'
temp_dir_w = 'dashubao/w/'


def get_temp(s, temp_dir=temp_dir_m):
    return "{0}{1}".format(temp_dir, s)


class M_IndexView(View):

    def get(self, request):

        all_noveldetail = modelhelp.get_all_book()

        fav_noveldetail = all_noveldetail.order_by("-novel_fav_nums", "-update_time")[:4]

        ids = []
        for item in fav_noveldetail:
            ids.append(item.id)

        create_noveldetail = all_noveldetail.exclude(id__in=ids).order_by("-create_time")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(create_noveldetail, 25)
        noveldetail = p.page(page)

        return render(request, get_temp("shuku-index.html"), {
            'noveldetail': noveldetail,
            'fav_noveldetail': fav_noveldetail,
        })


class Old_M_InfoView(View):
    def get(self, request, bookid):
        noveldetail = modelhelp.get_one_book({'novel_old_id': bookid})
        if noveldetail:
            return HttpResponseRedirect(noveldetail.get_info_path())

        return HttpResponseRedirect('/')

class M_InfoView(View):
    def get(self, request, bookid):

        isdaoxu = request.GET.get('isdaoxu', '')
        chapterid = request.GET.get('chapterid', 0)
        chapterid = int(chapterid)
        noveldetail = modelhelp.get_one_book({'url_md5': bookid})
        if noveldetail:
            all_chapter = noveldetail.get_book_chapter(isdaoxu=isdaoxu)
            if all_chapter:
                try:
                    page = request.GET.get('page', 1)
                except PageNotAnInteger:
                    page = 1
                p = Paginator(all_chapter, settings.WAP_CHAPTER_LIST)
                chapters = p.page(page)
                comefrom = help.encryption_urllib_base64(request.path)
                return render(request, get_temp("shuku-info.html"), {
                    'noveldetail': noveldetail,
                    'chapters': chapters,
                    'pagecount': range(1, chapters.paginator.num_pages + 1),
                    'isdaoxu': isdaoxu,
                    'chapterid': chapterid,
                    'comefrom': comefrom
                })



            return render(request, get_temp("error.html",temp_dir_p), {
                'message': '正在生成章节'
            })

        else:
            return render(request, get_temp("error.html",temp_dir_p), {
                'message': '本书暂时不能访问'
            })

        #return HttpResponseRedirect('/')


class Old_M_ContentView(View):
    def get(self, request, bookid, chapterid):
        chapter = modelhelp.get_one_chapter(kwargs={'chapter_old_id': chapterid})
        if chapter:
            return HttpResponseRedirect(chapter.get_content_path())

        return HttpResponseRedirect('/')


class M_ContentView(View):
    def get(self, request, chapterid):

        chapter = modelhelp.get_one_chapter(kwargs={'chapter_url_md5': chapterid})
        if chapter:
            page = math.ceil(chapter.chapter_order/settings.WAP_CHAPTER_LIST)
            if page <= 0:
                page = 1

            previous_chapter = modelhelp.get_previous_chapter(
                kwargs={'noveldetail': chapter.noveldetail, 'chapter_order__lt': chapter.chapter_order})

            next_chapter = modelhelp.get_next_chapter(
                kwargs={'noveldetail': chapter.noveldetail, 'chapter_order__gt': chapter.chapter_order})

            all_content = chapter.get_book_content()
            comefrom = help.encryption_urllib_base64(request.path)

            if all_content:
                content = all_content.first()
                spare_content = all_content.values('id', 'comefrom__comefrom')
            else:
                content = ''
                spare_content = ''

            return render(request, get_temp("shuku-content.html"), {
                'content': content,
                'spare_content': spare_content,
                'chapter': chapter,
                'previous_chapter': previous_chapter,
                'next_chapter': next_chapter,
                'comefrom': comefrom,
                'page': page
            })

        else:

            return render(request, get_temp("error.html",temp_dir_p), {
                'message': '正在生成章节'
            })

    def post(self, request, bookid, chapterid):

        cid = request.POST.get('cid', 0)
        cid = int(cid)
        try:
            content_obj = novels_models.NovelContent.objects.get(id=cid)
            return HttpResponse(content_obj.content, content_type='text/html')

        except Exception as e:
            logger.debug(e)
            return HttpResponse('', content_type='text/html')


class M_SortListView(View):

    def get(self, request, sortid):

        all_novelclassify = novels_models.NovelClassify.objects.all()
        status = request.GET.get('status', "2")
        status = int(status)
        other = request.GET.get('other', "all")
        kwargs = {}
        if sortid == 0:
            novelclassify = None

        else:
            novelclassify = all_novelclassify.filter(sortid=sortid).first()

            kwargs.update(novelclassify=sortid)

        # 连载
        if status == 0:
            kwargs.update(novel_status=0)

        elif status == 1:
            kwargs.update(novel_status=1)

        all_noveldetail = modelhelp.get_all_book(kwargs)

        if other == 'fav':
            all_noveldetail = all_noveldetail.order_by("-novel_fav_nums")
        elif other == 'zan':
            all_noveldetail = all_noveldetail.order_by("-novel_zan_nums")
        else:
            all_noveldetail = all_noveldetail.order_by("-create_time")


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_noveldetail, 10)
        noveldetail = p.page(page)

        return render(request, get_temp("shuku-categorylist.html"), {
            'all_novelclassify': all_novelclassify,
            'novelclassify': novelclassify,
            'all_noveldetail': noveldetail,
            'status': status,
            'other': other
        })

class M_HstoryBookshelfView(View):

    def get(self, request):
        return render(request, get_temp("shuku-historybookshelf.html"))





class IndexView(View):
    def get(self, request):
        all_noveldetail = modelhelp.get_all_book()

        create_noveldetail = all_noveldetail.order_by("-create_time")[:21]
        ids = []
        for item in create_noveldetail:
            ids.append(item.id)

        fav_noveldetail = all_noveldetail.exclude(id__in=ids).order_by("-novel_fav_nums","-update_time")[:6]

        for item in fav_noveldetail:
            ids.append(item.id)

        update_noveldetail = all_noveldetail.exclude(id__in=ids).order_by("-update_time")[:20]
        youqing = users_models.Links.objects.filter(ishide=False).order_by("-linkid")

        return render(request, get_temp("shuku-index.html",temp_dir_w),{
            'all_noveldetail': all_noveldetail,
            'fav_noveldetail': fav_noveldetail,
            'update_noveldetail': update_noveldetail,
            'create_noveldetail': create_noveldetail,
            'youqing': youqing
        })




class Old_InfoView(View):
    def get(self, request, pid, bookid):

        noveldetail = modelhelp.get_one_book({'novel_old_id': bookid})
        if noveldetail:
            return HttpResponseRedirect(noveldetail.get_info_path())

        return HttpResponseRedirect('/')


class InfoView(View):
    def get(self, request, bookid):
        isdaoxu = request.GET.get('isdaoxu', '')
        noveldetail = modelhelp.get_one_book({'url_md5': bookid})
        if noveldetail:
            all_chapter = noveldetail.get_book_chapter(isdaoxu=isdaoxu)
            if all_chapter:
                try:
                    page = request.GET.get('page', 1)
                except PageNotAnInteger:
                    page = 1
                p = Paginator(all_chapter, settings.WEB_CHAPTER_LIST)
                chapters = p.page(page)
                comefrom = help.encryption_urllib_base64(request.path)
                return render(request, get_temp("shuku-info.html",temp_dir_w), {
                    'noveldetail': noveldetail,
                    'chapters': chapters,
                    'isdaoxu': isdaoxu,
                    'comefrom': comefrom
                })

            return render(request, get_temp("error.html",temp_dir_p), {
                'message': '正在生成章节'
            })
        else:
            return render(request, get_temp("error.html",temp_dir_p), {
                'message': '本书暂时不能访问'
            })

class Old_ContentView(View):
    def get(self, request, pid , bookid, chapterid):
        chapter = modelhelp.get_one_chapter(kwargs={'chapter_old_id': chapterid})
        if chapter:
            return HttpResponseRedirect(chapter.get_content_path())

        return HttpResponseRedirect('/')


class ContentView(View):
    def get(self, request, chapterid):

        chapter = modelhelp.get_one_chapter(kwargs={'chapter_url_md5': chapterid})

        if chapter:
            page = math.ceil(chapter.chapter_order / settings.WEB_CHAPTER_LIST)
            if page <= 0:
                page = 1
            previous_chapter = modelhelp.get_previous_chapter(
                kwargs={'noveldetail': chapter.noveldetail, 'chapter_order__lt': chapter.chapter_order})

            next_chapter = modelhelp.get_next_chapter(
                kwargs={'noveldetail': chapter.noveldetail, 'chapter_order__gt': chapter.chapter_order})

            all_content = chapter.get_book_content()
            comefrom = help.encryption_urllib_base64(request.path)

            if all_content:
                content = all_content.first()
                spare_content = all_content.values('id', 'comefrom__comefrom')
            else:
                content = ''
                spare_content = ''

            return render(request, get_temp("shuku-content.html",temp_dir_w), {
                'content': content,
                'spare_content': spare_content,
                'chapter': chapter,
                'previous_chapter': previous_chapter,
                'next_chapter': next_chapter,
                'comefrom': comefrom,
                'page': page
            })

        else:

            return render(request, get_temp("error.html", temp_dir_p), {
                'message': '正在生成章节'
            })