import xadmin
from novels import models

class NovelClassifyAdmin(object):
    list_display = ['caption','sortid','create_time']
    search_fields = ['caption']
    # 筛选
    list_filter = ['create_time']




class NovelContentComefromAdmin(object):
    list_display = ['comefrom', 'comefrom_id']
    search_fields = ['comefrom']


class NovelDetailAdmin(object):
    list_display = ['novel_name', 'novel_author', 'create_time', 'update_time']
    search_fields = ['novel_name']
    # 筛选
    list_filter = ['novel_name']



xadmin.site.register(models.NovelDetail, NovelDetailAdmin)
xadmin.site.register(models.NovelClassify, NovelClassifyAdmin)
xadmin.site.register(models.NovelContentComefrom, NovelContentComefromAdmin)