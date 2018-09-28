

from django.db import models




class SearchCache(models.Model):
    searchtime = models.IntegerField(verbose_name="更新时间戳", default=0)
    keywords = models.CharField(max_length=60, verbose_name=u"搜索词")
    searchtype = models.CharField(max_length=8, choices=(("name", u"书名"), ("author", "作者")), default="name")
    results = models.SmallIntegerField(default=0, verbose_name=u"结果数量")
    ids = models.TextField(verbose_name=u"小说id")

    unique_together = [
        ('keywords', 'searchtype')
    ]