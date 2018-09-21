import xadmin
from operation import models



class UserAskAdmin(object):
    list_display = ['user', 'message', 'has_read', 'create_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'create_time']
    model_icon = 'fa fa-question-circle'



xadmin.site.register(models.UserAsk, UserAskAdmin)