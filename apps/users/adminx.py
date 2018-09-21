import xadmin
from xadmin import views


from dashubao.settings import GLOBALSETTINGS


class GlobalSettings(object):
    site_title = GLOBALSETTINGS['ADMIN_SITE_TITLE']
    site_footer = GLOBALSETTINGS['ADMIN_SITE_FOOTER']
    menu_style = "accordion"






xadmin.site.register(views.CommAdminView, GlobalSettings)