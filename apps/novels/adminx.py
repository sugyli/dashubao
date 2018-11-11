import xadmin
from novels import models
"""

list_display 控制列表展示的字段
search_fields 控制可以通过搜索框搜索的字段名称，xadmin使用的是模糊查询
list_filter 可以进行过滤操作的列
ordering 默认排序的字段
readonly_fields 在编辑页面的只读字段
exclude 在编辑页面隐藏的字段
list_editable 在列表页可以快速直接编辑的字段
show_detail_fileds 在列表页提供快速显示详情信息
refresh_times 指定列表页的定时刷新
list_export 控制列表页导出数据的可选格式
show_bookmarks 控制是否显示书签功能
data_charts 控制显示图标的样式
model_icon 控制菜单的图标


"""
class NovelChapterInline(object):
    model = models.NovelChapter
    extra = 0



class NovelClassifyAdmin(object):
    list_display = ['caption','sortid','create_time']
    search_fields = ['caption']
    # 筛选
    list_filter = ['create_time']




class NovelContentComefromAdmin(object):
    list_display = ['comefrom', 'comefrom_id']
    search_fields = ['comefrom']


class NovelDetailAdmin(object):
    # 在后台展示的字段
    list_display = ['novel_name', 'novel_author', 'create_time', 'update_time','novel_old_id','caiji_status','ishide','must_update','stop_update','laoshutongbu','id','get_admin_chapterList']
    # 可用来做搜索条件的字段（不用时间格式的字段
    search_fields = ['novel_name']
    # 用时间格式的字段做过滤器筛选字段
    list_filter = ['update_time','iswenziname','have_chapter','stop_update','caiji_status','ishide','laoshutongbu']
    # 设置可以在列表中直接修改的字段
    list_editable = ['stop_update','must_update','ishide','laoshutongbu']

    ordering = ['-update_time']
    #inlines = [NovelChapterInline]
    # 设置自动刷新
    #refresh_times = [5, 7]
    # 配置插件效果
    #style_fields = {'content': 'ueditor'}
#
# class NovelChapterAdmin(object):
#     list_display = ['chapter_name']
#     search_fields = ['noveldetail__url_md5']
#     list_filter = ['update_time','ishide']
#     list_per_page = 10

    #hidden_menu = True




xadmin.site.register(models.NovelDetail, NovelDetailAdmin)
#xadmin.site.register(models.NovelClassify, NovelClassifyAdmin)
#xadmin.site.register(models.NovelContentComefrom, NovelContentComefromAdmin)
#xadmin.site.register(models.NovelChapter, NovelChapterAdmin)