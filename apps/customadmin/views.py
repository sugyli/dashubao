import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from novels import models as novels_models

def get_temp(s):
    return "{0}{1}".format('dashubao/customadmin/', s)

def VerificationLogin(request):

    if request.user.is_authenticated and request.user.is_superuser == 1:
        return True
    else:
        return False


class ChapterList(View):

    def get(self, request, bookid):
        if VerificationLogin(request):

            noveldetail_data = novels_models.NovelDetail.objects.filter(url_md5=bookid).first()
            ishide = request.GET.get('ishide', '')
            weipipei = request.GET.get('weipipei', '')

            kwargs = {}
            if ishide == '0' or ishide == '1':
                kwargs.update(ishide=ishide)
            if weipipei:
                chapter_datas = noveldetail_data.novelchapter_set.filter(ishide=0).exclude(fenbiao=1,chapter_old_id__gt=0).order_by("chapter_order")
            else:
                chapter_datas = noveldetail_data.novelchapter_set.filter(**kwargs).order_by("chapter_order")

            # ishide = request.GET.get('ishide', 0)
            #
            # count = request.GET.get('count', 30)
            # count = int(count)
            # if count >= 10000:
            #     count = 10000
            # kwargs = {}
            # if ishide:
            #     kwargs.update(ishide = ishide)
            # all_chapter_datas = noveldetail_data.novelchapter_set.filter(**kwargs).order_by("chapter_order")
            # try:
            #     page = request.GET.get('page', 1)
            # except PageNotAnInteger:
            #     page = 1
            #
            # p = Paginator(all_chapter_datas, count)
            # chapter_datas = p.page(page)


            return render(request, get_temp("chapterList.html"),{
                'chapter_datas': chapter_datas,
                'noveldetail_data': noveldetail_data,
                'ishide': ishide,
                'weipipei': weipipei
            })

        else:
            return HttpResponseRedirect('/')
    def post(self, request , bookid):

        if VerificationLogin(request):
            custom = request.POST.get('custom', '')
            if custom == 'pipeiid':
                chapter_id = request.POST.get('chapter_id', '')
                old_chapter_id = request.POST.get('old_chapter_id', '')

                if chapter_id and old_chapter_id:
                    chapter_id = chapter_id.split(',')
                    old_chapter_id = old_chapter_id.split(',')

                    if len(old_chapter_id) == len(chapter_id):
                        new_array = list(zip(old_chapter_id, chapter_id))
                        mes = ''
                        for _ in new_array:
                            if _[0] != _[1]:

                                old_chapter = novels_models.NovelChapter.objects.filter(id=_[0]).first()

                                chapter = novels_models.NovelChapter.objects.filter(id=_[1]).first()

                                if old_chapter and chapter:
                                    chapter.chapter_old_id = old_chapter.chapter_old_id
                                    #chapter.chapter_url_md5 = old_chapter.chapter_url_md5

                                    old_content = old_chapter.get_book_content(kwargs = {'comefrom__id':1}, ishide = False)
                                    if old_content:
                                        content = chapter.get_book_content(kwargs = {'comefrom__id': 1}, ishide = False)

                                        if content:
                                            content[0].content = old_content[0].content
                                            content[0].num_words = old_content[0].num_words
                                            content[0].content_url = old_content[0].content_url
                                            content[0].save()
                                        else:
                                            kwargs = {
                                                'content':old_content[0].content,
                                                'num_words': old_content[0].num_words,
                                                'content_url': old_content[0].content_url,
                                                'content_url_md5': old_content[0].content_url_md5,
                                                'comefrom': old_content[0].comefrom,
                                            }
                                            chapter.add_book_content(kwargs)

                                        old_content[0].delete()
                                        old_chapter.delete()
                                        mes += '老ID %s 处理成功 ' % _[0]

                                    else:
                                        old_chapter.delete()
                                        mes += '老ID %s 内容不存在删除老章节属于正常 ' % _[0]

                                    chapter.save()

                                else:

                                    mes += '老ID %s 不存在 '%_[0]
                            else:

                                mes += '老ID %s 和新ID重复了 ' % _[0]


                        return HttpResponse('{"status":"success","msg":"%s"}'%mes, content_type='application/json')


                    else:

                        return HttpResponse('{"status":"fail","msg":"章节数量不对"}', content_type='application/json')

                else:

                    return HttpResponse('{"status":"fail","msg":"chapter_id old_chapter_id出错了"}', content_type='application/json')
            elif custom == 'showneirong':
                chapterid = request.POST.get('chapterid', '')
                chapter = novels_models.NovelChapter.objects.filter(chapter_url_md5 = chapterid).first()
                if chapter:
                    content = chapter.novelcontent_set.filter(comefrom__id = 1).first()
                    data = {
                        "data":""
                    }
                    if content:
                        data['data'] = content.content
                    return HttpResponse(json.dumps(data), content_type='application/json')

                else:
                    return HttpResponse('{"status":"fail","msg":"章节不存在"}', content_type='application/json')

            elif custom == 'delchapter':
                chapterids = request.POST.get('chapterids', '')
                chapterids = chapterids.strip()
                if chapterids:
                    chapterids = chapterids.split(',')
                    msg = ''
                    for chapterid in chapterids:
                        chapter = novels_models.NovelChapter.objects.filter(id=chapterid).first()
                        if chapter:
                            contents = chapter.get_book_content(ishide=False)
                            if contents:
                                contents.delete()
                                msg += "章节编号%s大书包的内容已经删除," % chapterid
                            else:
                                msg += "编号%s内容不存在," % chapterid
                            chapter.delete()
                            msg += "编号%s章节已经删除,"%chapterid

                        else:
                            msg += "编号%s章节不存在,"%chapterid


                    return HttpResponse('{"status":"success","msg":"%s"}' % msg,content_type='application/json')

                else:
                    return HttpResponse('{"status":"fail","msg":"chapterids 不能为空"}', content_type='application/json')

            else:

                return HttpResponse('{"status":"fail","msg":"custom 非法"}', content_type='application/json')

        else:
            return HttpResponse('{"status":"fail","msg":"还没有登录"}', content_type='application/json')



