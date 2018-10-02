import datetime
import logging

from django.db import models

from users import models as users_models
from novels import models as novels_models
from utils import modelhelp

logger = logging.getLogger(__name__)

# Create your models here.

class UserZan(models.Model):
    user = models.ForeignKey(users_models.UserProfile,on_delete=models.CASCADE, verbose_name=u"用户")
    novel = models.ForeignKey(novels_models.NovelDetail,to_field='url_md5',on_delete=models.CASCADE, verbose_name=u"小说")
    create_time = models.DateTimeField(default=datetime.date.today, verbose_name=u"添加时间")


    class Meta:
        verbose_name = u"用户点赞"
        verbose_name_plural = verbose_name


    def __str__(self):
        return '用户({0})'.format(self.user.username)

class NovelFavorite(models.Model):
    user = models.ForeignKey(users_models.UserProfile, on_delete=models.CASCADE, verbose_name=u"用户")
    novel = models.ForeignKey(novels_models.NovelDetail,to_field='url_md5', on_delete=models.CASCADE, verbose_name=u"小说")
    chapterid = models.CharField(max_length=50, verbose_name=u"章节ID" , default =0)
    create_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u"更新时间")
    update_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u"更新时间")
    chapter = None
    new_chapter = None
    class Meta:
        index_together = [
            ["user","novel","chapterid"],
        ]
        unique_together = [
            ('user','novel')
        ]
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name


    def get_chapter(self):
        if self.chapter is None:
            self.chapter = modelhelp.get_one_chapter(kwargs={'chapter_url_md5': self.chapterid})

        return self.chapter


    def get_favchaptername(self):
        chapter = self.get_chapter()
        if chapter:
            return chapter.chapter_name
        return chapter

    def get_favchapterurl(self):
        chapter = self.get_chapter()
        if chapter:
            return chapter.get_content_path
        return chapter



    def get_new_chapter(self):

        if self.new_chapter is None:
            self.new_chapter = modelhelp.get_all_chapter(isdaoxu=True,kwargs={'noveldetail': self.novel}).last()

        return self.new_chapter

    def have_new_chapter(self):

        try:
            chapter = self.get_new_chapter()
            if chapter.update_time > self.update_time:
                return True

            return False
        except Exception as e:
            logger.debug(e)
            return False


