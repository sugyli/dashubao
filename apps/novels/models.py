from datetime import datetime

from django.db import models
from django.shortcuts import reverse

#from utils import help
from utils import modelhelp

class NovelContentComefrom(models.Model):
    comefrom = models.CharField(max_length=20, verbose_name=u"来源网站", unique=True)
    comefrom_id = models.PositiveSmallIntegerField(
        default=0, verbose_name=u"权重", unique=True)
    ishide = models.BooleanField(
        default=False,
        verbose_name=u"是否隐藏")

    class Meta:
        verbose_name = u"小说内容来源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comefrom


class NovelClassify(models.Model):
    caption = models.CharField(max_length=20, verbose_name=u"分类", unique=True)
    sortid = models.PositiveSmallIntegerField(
        default=0, verbose_name=u"分类ID")
    create_time = models.DateTimeField(
        default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"小说分类"
        verbose_name_plural = verbose_name

    def get_sortlist_path(self):

        return reverse('novels:novels_sortlist', args=[self.sortid])

    def __str__(self):
        return self.caption


class NovelDetail(models.Model):
    url = models.CharField(max_length=500, verbose_name=u"来源地址")
    url_md5 = models.CharField(
        max_length=50,
        verbose_name=u"查询主键",
        unique=True)
    novel_name = models.CharField(max_length=300, verbose_name=u"小说名")
    slug = models.CharField(max_length=500, verbose_name=u"拼音",default='')
    quanping = models.CharField(max_length=500, verbose_name=u"拼音", default='')

    novel_author = models.CharField(max_length=300, verbose_name=u"作者")
    novel_comefrom = models.CharField(
        max_length=20,
        verbose_name=u"来源网站",
        default='',
        )
    novel_info = models.TextField(
        default='',
        verbose_name=u"小说简介",
        null=True,
        blank=True)
    create_time = models.DateTimeField(
        default=datetime.now, verbose_name=u"添加时间")
    update_time = models.DateTimeField(
        default=datetime.now, verbose_name=u"更新时间")
    novel_old_id = models.IntegerField(
        default=0, verbose_name=u"对于老站编号", null=True, blank=True)
    novel_fav_nums = models.IntegerField(
        default=0,
        verbose_name=u'收藏人数',
        null=True,
        blank=True)
    novel_zan_nums = models.IntegerField(
        default=0, verbose_name=u'推荐人数', null=True, blank=True)
    novel_click_nums = models.IntegerField(
        default=0,
        verbose_name=u"点击数",
        null=True,
        blank=True)
    novel_status = models.BooleanField(default=False, verbose_name=u"是否完本",null=True, blank=True)
    ishide = models.BooleanField(
        default=False,
        verbose_name=u"是否隐藏",null=True, blank=True)
    have_chapter = models.BooleanField(
        default=False,
        verbose_name=u"是否有章节", null=True, blank=True)
    stop_update = models.BooleanField(
        default=False,
        verbose_name=u"采集更新",null=True, blank=True)
    image = models.ImageField(
        upload_to="courses/%Y/%m/%d",
        default="",
        verbose_name=u"封面图",
        max_length=300, null=True, blank=True)
    novelclassify = models.ForeignKey(
        NovelClassify,
        on_delete=models.SET_NULL,
        verbose_name=u"小说类型",
        default=0, null=True,
        blank=True)


    all_chapter = None

    class Meta:
        index_together = [
            ["novel_old_id"],
        ]
        unique_together = [
            ('novel_name', 'novel_author', 'novel_comefrom')
        ]
        verbose_name = u"小说详情"
        verbose_name_plural = verbose_name

    def get_image_path(self):
        return self.image

    def get_info_path(self):

        return reverse('novels:novels_info', args=[self.slug,self.url_md5])

        # if self.novel_old_id > 0:
        #     return reverse('novels_info', args=[self.novel_old_id])
        # else:
        #     return reverse('novels:novels_info', args=[self.url_md5])

    def get_book_status(self):
        if self.novel_status > 0:
            return '完本'
        else:
            return '连载中'

    def get_book_chapter(self, isdaoxu=None):

        if self.all_chapter is None:

            self.all_chapter = modelhelp.get_all_chapter(isdaoxu=isdaoxu, kwargs={'noveldetail': self.url_md5})

        return self.all_chapter


    def get_first_chapter(self):
        return self.get_book_chapter().order_by('chapter_order').first()

        #return reverse('novels:novels_content', args=[first_chapter.chapter_url_md5])

        # if first_chapter.chapter_old_id > 0:
        #     yield reverse('novels_content', args=[first_chapter.noveldetail.novel_old_id,first_chapter.chapter_old_id])
        # else:
        #     yield reverse('novels:novels_content',args=[first_chapter.noveldetail.url_md5,first_chapter.chapter_url_md5])

    def get_last_chapter(self):

        return self.get_book_chapter().order_by('chapter_order').last()


    def __str__(self):
        return self.novel_name


class NovelChapter(models.Model):
    noveldetail = models.ForeignKey(
        NovelDetail,
        on_delete=models.CASCADE,
        verbose_name=u"小说详情",
        to_field='url_md5',
        default='')
    chapter_url = models.CharField(
        max_length=500,
        verbose_name=u"来源地址",
        default='')
    chapter_url_md5 = models.CharField(
        max_length=50,
        verbose_name=u"查询主键",
        unique=True, default='')
    chapter_name = models.CharField(max_length=300, verbose_name=u"章节名")
    create_time = models.DateTimeField(
        default=datetime.now, verbose_name=u"添加时间")
    update_time = models.DateTimeField(
        default=datetime.now, verbose_name=u"更新时间")
    chapter_type = models.BooleanField(default=False, verbose_name=u"是否为卷标")
    ishide = models.BooleanField(
        default=False,
        verbose_name=u"是隐藏",
        null=True,
        blank=True)
    chapter_order = models.SmallIntegerField(default=0, verbose_name=u"排序")
    chapter_old_id = models.IntegerField(
        default=0, verbose_name=u"对于老站编号")

    class Meta:
        verbose_name = u"小说章节"
        verbose_name_plural = verbose_name

    def get_content_path(self):

        return reverse('novels:novels_content',args=[self.chapter_url_md5])

        # if self.chapter_old_id > 0:
        #     return reverse(
        #         'novels_content',
        #         args=[
        #             self.noveldetail.novel_old_id,
        #             self.chapter_old_id])
        # else:
        #
        #     return reverse(
        #         'novels:novels_content',
        #         args=[
        #             self.noveldetail.url_md5,
        #             self.chapter_url_md5])

    def get_book_content(self):
        return self.novelcontent_set.filter(ishide=0).order_by("-comefrom")


    def __str__(self):
        return self.chapter_name


class NovelContent(models.Model):
    comefrom = models.ForeignKey(
        NovelContentComefrom,
        on_delete=models.SET_NULL,
        to_field='comefrom_id',
        verbose_name=u"小说来源",
        default='', null=True,
        blank=True)
    content = models.TextField(verbose_name=u"小说内容")
    chapter = models.ManyToManyField(NovelChapter,through='ChapterContent')
    num_words = models.IntegerField(
        default=0, verbose_name=u"统计字数", null=True, blank=True)

    content_url = models.CharField(
        max_length=500,
        verbose_name=u"来源地址",
        default='')
    content_url_md5 = models.CharField(
        max_length=50,
        verbose_name=u"查询主键",
        unique=True, default='')
    create_time = models.DateTimeField(
        default=datetime.now, verbose_name=u"添加时间")
    update_time = models.DateTimeField(
        default=datetime.now, verbose_name=u"更新时间")
    ishide = models.BooleanField(
        default=False,
        verbose_name=u"是否隐藏",
        null=True,
        blank=True)


class ChapterContent(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelContent,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]
