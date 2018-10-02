import time

from django.shortcuts import render
from django.views.generic import View
from django.conf import settings


from search import models as search_models
from novels import models as novels_models
from utils import modelhelp


# Create your views here.

temp_dir_m = 'dashubao/m/'
temp_dir_p = 'dashubao/p/'
temp_dir_w = 'dashubao/w/'

def get_temp(s, temp_dir=temp_dir_m):
    return "{0}{1}".format(temp_dir, s)

class M_SearchView(View):
    def get(self, request):
        q = request.GET.get('q','')
        q = q.strip()
        s_type = request.GET.get("s_type", "name")
        now_time = int(time.time())
        sct = settings.SCT
        list_count = 50
        ls = ''
        n_result = ''

        if q:
            if s_type == 'author':
                s_result = search_models.SearchCache.objects.filter(keywords=q,searchtype=s_type).first()

                if s_result and now_time - s_result.searchtime <= sct:
                    ids = s_result.ids
                    ids = ids.split(',')
                    ordering = 'FIELD(`url_md5`, %s)' % ','.join("'%s'" % str(id) for id in ids)

                    n_result = modelhelp.get_all_book(kwargs={'url_md5__in': ids}).extra(select={'ordering': ordering},order_by=('ordering',))[:list_count]

                else:
                    n_result = modelhelp.get_all_book(kwargs={'novel_author__icontains': q})[:list_count]

                    if n_result:
                        ids = n_result.values('url_md5')
                        ids = [r['url_md5'] for r in ids]
                        ids_count = len(ids)
                        ids = ','.join(ids)
                        s_obj,created = search_models.SearchCache.objects.get_or_create(keywords=q,searchtype=s_type)
                        s_obj.ids = ids
                        s_obj.results = ids_count
                        s_obj.searchtime = now_time
                        s_obj.save()

            else:

                s_result = search_models.SearchCache.objects.filter(keywords=q, searchtype='name').first()

                if s_result and now_time - s_result.searchtime <= sct:

                    ids = s_result.ids
                    ids = ids.split(',')
                    ordering = 'FIELD(`url_md5`, %s)' % ','.join("'%s'"%str(id) for id in ids)

                    n_result = modelhelp.get_all_book(kwargs={'url_md5__in': ids}).extra(select={'ordering': ordering}, order_by=('ordering',))[:list_count]

                else:

                    n_result = modelhelp.get_all_book(kwargs={'novel_name__icontains':q})[:list_count]
                    if n_result:
                        ids = n_result.values('url_md5')
                        ids = [r['url_md5'] for r in ids]
                        ids_count = len(ids)
                        ids = ','.join(ids)
                        s_obj,created = search_models.SearchCache.objects.get_or_create(keywords=q,searchtype='name')
                        s_obj.ids = ids
                        s_obj.results = ids_count
                        s_obj.searchtime = now_time
                        s_obj.save()

        else:
            s = search_models.SearchCache.objects.all().order_by('-searchtime')[:18]
            a = []

            if s:
                for r in s:
                    ids = r.ids.split(',')
                    for id in ids:
                        a.append(id)

                b = list(set(a))
                b.sort(key=a.index)
                ordering = 'FIELD(`url_md5`, %s)' % ','.join("'%s'" % str(id) for id in b)



                ls = modelhelp.get_all_book(kwargs={'url_md5__in': b}).extra(select={'ordering': ordering}, order_by=('ordering',))[:18]


        return render(request, get_temp("shuku-search.html"),{
            's_type':s_type,
            'result': n_result,
            'ls': ls,
            'q': q
        })