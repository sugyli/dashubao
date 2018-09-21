from datetime import datetime

from django.db import models

from users import models as users_models
from novels import models as novels_models

# Create your models here.
class UserAsk(models.Model):
    user = models.ForeignKey(users_models.UserProfile,on_delete=models.CASCADE, verbose_name=u"提问用户")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    comefrom = models.CharField(max_length=500, verbose_name=u"来路" ,default='')
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name


    def __str__(self):
        return '用户({0})'.format(self.user.username)



class UserZan(models.Model):
    user = models.ForeignKey(users_models.UserProfile,on_delete=models.CASCADE, verbose_name=u"用户")
    novel = models.ForeignKey(novels_models.NovelDetail,to_field='url_md5',on_delete=models.CASCADE, verbose_name=u"小说")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


    class Meta:
        unique_together = [
            ('user','novel')
        ]
        verbose_name = u"用户点赞"
        verbose_name_plural = verbose_name


    def __str__(self):
        return '用户({0})'.format(self.user.username)





class NovelFavorite(models.Model):
    user = models.ForeignKey(users_models.UserProfile, on_delete=models.CASCADE, verbose_name=u"用户")
    novel = models.ForeignKey(novels_models.NovelDetail,to_field='url_md5', on_delete=models.CASCADE, verbose_name=u"小说")
    chapterid = models.CharField(max_length=50, verbose_name=u"章节主键",default='',null=True,blank=True)
    update_time = models.DateTimeField(default=datetime.now, verbose_name=u"更新时间")

    class Meta:
        unique_together = [
            ('user','novel')
        ]
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name
