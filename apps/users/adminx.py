import xadmin
from xadmin import views
from users import models

from dashubao.settings import GLOBALSETTINGS


class GlobalSettings(object):
    site_title = GLOBALSETTINGS['ADMIN_SITE_TITLE']
    site_footer = GLOBALSETTINGS['ADMIN_SITE_FOOTER']
    menu_style = "accordion"


class LinksAdmin(object):
    list_display = ['name', 'url','linkid']
    search_fields = ['name']

class UserAskAdmin(object):
    list_display = ['user', 'message', 'has_read', 'create_time']
    search_fields = ['user', 'has_read']
    list_filter = ['user', 'has_read', 'create_time']
    model_icon = 'fa fa-question-circle'

xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(models.Links, LinksAdmin)
xadmin.site.register(models.UserAsk, UserAskAdmin)