from datetime import datetime

from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

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

        return reverse('novels:novels_sortlist', args=[self.id])

    def __str__(self):
        return self.caption

class NovelTag(models.Model):
    caption = models.CharField(max_length=20, verbose_name=u"tag", unique=True)
    tagid = models.PositiveSmallIntegerField(
        default=0, verbose_name=u"tagid")
    create_time = models.DateTimeField(
        default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"小说Tag"
        verbose_name_plural = verbose_name

    # def get_sortlist_path(self):
    #
    #     return reverse('novels:novels_sortlist', args=[self.tagid])

    def __str__(self):
        return self.caption


class NovelDetail(models.Model):
    url_md5 = models.CharField(
        max_length=50,
        verbose_name=u"查询主键",
        unique=True)
    url = models.CharField(max_length=500, verbose_name=u"来源地址")
    caiji_url_md5 = models.CharField(default='',max_length=50,verbose_name=u"判断采集url",unique=True)

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
        default=0, verbose_name=u"老书", null=True, blank=True)
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

    iswenziname = models.BooleanField(default=True,verbose_name=u"标题文字",null=True, blank=True)

    have_chapter = models.BooleanField(
        default=False,
        verbose_name=u"是否有章节", null=True, blank=True)
    stop_update = models.BooleanField(
        default=False,
        verbose_name=u"停止更新",null=True, blank=True)
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

    caiji_status = models.CharField(default='ys',verbose_name=u"采集状态", choices=(("ys", "原始"), ("th", "替换"), ("tj", "添加")), max_length=2)

    tag = models.ManyToManyField(NovelTag)

    chapter_nums = models.IntegerField(
        default=0,
        verbose_name=u"章节数",
        null=True,
        blank=True)
    must_update = models.BooleanField(
        default=False,
        verbose_name=u"强制更新", null=True, blank=True)
    laoshutongbu = models.BooleanField(
        default=False,
        verbose_name=u"老书同步", null=True, blank=True)

    all_chapter = None

    class Meta:
        index_together = [
            ["novel_old_id"],
            ["have_chapter"],
            ["iswenziname"],
            ["stop_update"],
            ["ishide"],
            ["create_time"],
            ["update_time"],
            ["caiji_status"],
            ["must_update"],
            ["laoshutongbu"]
        ]
        unique_together = [
            ('novel_name', 'novel_author', 'novel_comefrom')
        ]
        verbose_name = u"小说详情"
        verbose_name_plural = verbose_name

    def get_image_path(self):
        return "{0}{1}".format(settings.FENMIAN_URL,self.image)

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

    def get_admin_chapterList_url(self):
        return reverse('customadmin:customadmin_chapterList', args=[self.url_md5])

    def get_admin_chapterList(self):
        url = self.get_admin_chapterList_url()
        return mark_safe("<a href='%s' target='_blank'>跳转</>"%url)
    get_admin_chapterList.short_description = "章节"


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

    fenbiao = models.BooleanField(
        default=False,
        verbose_name=u"内容分表", null=True, blank=True)

    chapter_order = models.SmallIntegerField(default=0, verbose_name=u"排序")
    chapter_old_id = models.IntegerField(
        default=0, verbose_name=u"对于老站编号", null=True, blank=True)

    class Meta:
        index_together = [
            ["fenbiao"],
            ["ishide"],
            ["chapter_order"],
            ["chapter_old_id"],
            ["chapter_type"],
            ["create_time"],
            ["update_time"]
        ]
        # unique_together = [
        #     ('noveldetail', 'chapter_order')
        # ]
        verbose_name = u"小说章节"
        verbose_name_plural = verbose_name

    def get_ishide(self):
        if self.ishide == 1:
            return '隐藏'
        else:
            return '显示'

    def get_laoshuneirongzhuangtai(self):
        if self.fenbiao == 1 and self.chapter_old_id > 0:
            return '老章节以匹配'
        elif self.fenbiao == 1 and self.chapter_old_id == 0:
            return '新章节'
        elif self.fenbiao == 0 and self.chapter_old_id > 0:
            return '老章节没匹配'
        else:
            return '未知情况'


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

    def get_book_content(self,kwargs={},ishide =True):
        if ishide:
            kwargs.update(ishide=0)
        if self.fenbiao:
            id = str(self.id)
            last_nb = id[-1]
            if last_nb == '1':
                return self.novelnewcontentone_set.filter(**kwargs).order_by("-comefrom")
            elif last_nb == '2':
                return self.novelnewcontenttwo_set.filter(**kwargs).order_by("-comefrom")
            elif last_nb == '3':
                return self.novelnewcontentthree_set.filter(**kwargs).order_by("-comefrom")
            elif last_nb == '4':
                return self.novelnewcontentfour_set.filter(**kwargs).order_by("-comefrom")
            elif last_nb == '5':
                return self.novelnewcontentfive_set.filter(**kwargs).order_by("-comefrom")
            elif last_nb == '6':
                return self.novelnewcontentsix_set.filter(**kwargs).order_by("-comefrom")
            elif last_nb == '7':
                return self.novelnewcontentseven_set.filter(**kwargs).order_by("-comefrom")
            elif last_nb == '8':
                return self.novelnewcontenteight_set.filter(**kwargs).order_by("-comefrom")
            elif last_nb == '9':
                return self.novelnewcontentnine_set.filter(**kwargs).order_by("-comefrom")
            else:
                return self.novelnewcontent_set.filter(**kwargs).order_by("-comefrom")

        return self.novelcontent_set.filter(**kwargs).order_by("-comefrom")

    def add_book_content(self,kwargs={}):
        id = str(self.id)
        last_nb = id[-1]
        if last_nb == '1':

            content = NovelNewContentOne.objects.create(**kwargs)
            return ChapterNewContentOne.objects.create(novelchapter=self,novelcontent=content)

        elif last_nb == '2':
            content = NovelNewContentTwo.objects.create(**kwargs)
            return ChapterNewContentTwo.objects.create(novelchapter=self,novelcontent=content)

        elif last_nb == '3':
            content = NovelNewContentThree.objects.create(**kwargs)
            return ChapterNewContentThree.objects.create(novelchapter=self,novelcontent=content)

        elif last_nb == '4':
            content = NovelNewContentFour.objects.create(**kwargs)
            return ChapterNewContentFour.objects.create(novelchapter=self,novelcontent=content)

        elif last_nb == '5':
            content = NovelNewContentFive.objects.create(**kwargs)
            return ChapterNewContentFive.objects.create(novelchapter=self,novelcontent=content)

        elif last_nb == '6':
            content = NovelNewContentSix.objects.create(**kwargs)
            return ChapterNewContentSix.objects.create(novelchapter=self,novelcontent=content)

        elif last_nb == '7':
            content = NovelNewContentSeven.objects.create(**kwargs)
            return ChapterNewContentSeven.objects.create(novelchapter=self,novelcontent=content)


        elif last_nb == '8':
            content = NovelNewContentEight.objects.create(**kwargs)
            return ChapterNewContentEight.objects.create(novelchapter=self,novelcontent=content)


        elif last_nb == '9':
            content = NovelNewContentNine.objects.create(**kwargs)
            return ChapterNewContentNine.objects.create(novelchapter=self,novelcontent=content)

        else:
            content = NovelNewContent.objects.create(**kwargs)
            return ChapterNewContent.objects.create(novelchapter=self,novelcontent=content)

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
        verbose_name=u"是隐藏",
        null=True,
        blank=True)

    class Meta:
        index_together = [
            ["ishide"],
        ]
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name


class ChapterContent(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelContent,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    isdel = models.BooleanField(default=False,verbose_name=u"是否删除",null=True,blank=True)

    class Meta:
        index_together = [
            ["isdel"],
        ]
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]


class NovelNewContent(models.Model):
    comefrom = models.ForeignKey(
        NovelContentComefrom,
        on_delete=models.SET_NULL,
        to_field='comefrom_id',
        verbose_name=u"小说来源",
        default='', null=True,
        blank=True)
    content = models.TextField(verbose_name=u"小说内容")
    chapter = models.ManyToManyField(NovelChapter,through='ChapterNewContent')
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
        verbose_name=u"是隐藏",
        null=True,
        blank=True)

    class Meta:
        index_together = [
            ["ishide"],
        ]
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name

class ChapterNewContent(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelNewContent,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    isdel = models.BooleanField(default=False, verbose_name=u"是否删除", null=True, blank=True)

    class Meta:
        index_together = [
            ["isdel"],
        ]
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]


class NovelNewContentOne(models.Model):
    comefrom = models.ForeignKey(
        NovelContentComefrom,
        on_delete=models.SET_NULL,
        to_field='comefrom_id',
        verbose_name=u"小说来源",
        default='', null=True,
        blank=True)
    content = models.TextField(verbose_name=u"小说内容")
    chapter = models.ManyToManyField(NovelChapter,through='ChapterNewContentOne')
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
        verbose_name=u"是隐藏",
        null=True,
        blank=True)

    class Meta:
        index_together = [
            ["ishide"],
        ]
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name

class ChapterNewContentOne(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelNewContentOne,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    isdel = models.BooleanField(default=False, verbose_name=u"是否删除", null=True, blank=True)

    class Meta:
        index_together = [
            ["isdel"],
        ]
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]


class NovelNewContentTwo(models.Model):
    comefrom = models.ForeignKey(
        NovelContentComefrom,
        on_delete=models.SET_NULL,
        to_field='comefrom_id',
        verbose_name=u"小说来源",
        default='', null=True,
        blank=True)
    content = models.TextField(verbose_name=u"小说内容")
    chapter = models.ManyToManyField(NovelChapter,through='ChapterNewContentTwo')
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
        verbose_name=u"是隐藏",
        null=True,
        blank=True)

    class Meta:
        index_together = [
            ["ishide"],
        ]
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name

class ChapterNewContentTwo(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelNewContentTwo,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    isdel = models.BooleanField(default=False, verbose_name=u"是否删除", null=True, blank=True)

    class Meta:
        index_together = [
            ["isdel"],
        ]
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]


class NovelNewContentThree(models.Model):
    comefrom = models.ForeignKey(
        NovelContentComefrom,
        on_delete=models.SET_NULL,
        to_field='comefrom_id',
        verbose_name=u"小说来源",
        default='', null=True,
        blank=True)
    content = models.TextField(verbose_name=u"小说内容")
    chapter = models.ManyToManyField(NovelChapter,through='ChapterNewContentThree')
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
        verbose_name=u"是隐藏",
        null=True,
        blank=True)

    class Meta:
        index_together = [
            ["ishide"],
        ]
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name

class ChapterNewContentThree(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelNewContentThree,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    isdel = models.BooleanField(default=False, verbose_name=u"是否删除", null=True, blank=True)

    class Meta:
        index_together = [
            ["isdel"],
        ]
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]


class NovelNewContentFour(models.Model):
    comefrom = models.ForeignKey(
        NovelContentComefrom,
        on_delete=models.SET_NULL,
        to_field='comefrom_id',
        verbose_name=u"小说来源",
        default='', null=True,
        blank=True)
    content = models.TextField(verbose_name=u"小说内容")
    chapter = models.ManyToManyField(NovelChapter,through='ChapterNewContentFour')
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
        verbose_name=u"是隐藏",
        null=True,
        blank=True)

    class Meta:
        index_together = [
            ["ishide"],
        ]
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name

class ChapterNewContentFour(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelNewContentFour,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    isdel = models.BooleanField(default=False, verbose_name=u"是否删除", null=True, blank=True)

    class Meta:
        index_together = [
            ["isdel"],
        ]
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]


class NovelNewContentFive(models.Model):
    comefrom = models.ForeignKey(
        NovelContentComefrom,
        on_delete=models.SET_NULL,
        to_field='comefrom_id',
        verbose_name=u"小说来源",
        default='', null=True,
        blank=True)
    content = models.TextField(verbose_name=u"小说内容")
    chapter = models.ManyToManyField(NovelChapter,through='ChapterNewContentFive')
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
        verbose_name=u"是隐藏",
        null=True,
        blank=True)

    class Meta:
        index_together = [
            ["ishide"],
        ]
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name

class ChapterNewContentFive(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelNewContentFive,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    isdel = models.BooleanField(default=False, verbose_name=u"是否删除", null=True, blank=True)

    class Meta:
        index_together = [
            ["isdel"],
        ]
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]


class NovelNewContentSix(models.Model):
    comefrom = models.ForeignKey(
        NovelContentComefrom,
        on_delete=models.SET_NULL,
        to_field='comefrom_id',
        verbose_name=u"小说来源",
        default='', null=True,
        blank=True)
    content = models.TextField(verbose_name=u"小说内容")
    chapter = models.ManyToManyField(NovelChapter,through='ChapterNewContentSix')
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
        verbose_name=u"是隐藏",
        null=True,
        blank=True)

    class Meta:
        index_together = [
            ["ishide"],
        ]
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name

class ChapterNewContentSix(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelNewContentSix,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    isdel = models.BooleanField(default=False, verbose_name=u"是否删除", null=True, blank=True)

    class Meta:
        index_together = [
            ["isdel"],
        ]
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]


class NovelNewContentSeven(models.Model):
    comefrom = models.ForeignKey(
        NovelContentComefrom,
        on_delete=models.SET_NULL,
        to_field='comefrom_id',
        verbose_name=u"小说来源",
        default='', null=True,
        blank=True)
    content = models.TextField(verbose_name=u"小说内容")
    chapter = models.ManyToManyField(NovelChapter,through='ChapterNewContentSeven')
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
        verbose_name=u"是隐藏",
        null=True,
        blank=True)

    class Meta:
        index_together = [
            ["ishide"],
        ]
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name

class ChapterNewContentSeven(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelNewContentSeven,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    isdel = models.BooleanField(default=False, verbose_name=u"是否删除", null=True, blank=True)

    class Meta:
        index_together = [
            ["isdel"],
        ]
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]


class NovelNewContentEight(models.Model):
    comefrom = models.ForeignKey(
        NovelContentComefrom,
        on_delete=models.SET_NULL,
        to_field='comefrom_id',
        verbose_name=u"小说来源",
        default='', null=True,
        blank=True)
    content = models.TextField(verbose_name=u"小说内容")
    chapter = models.ManyToManyField(NovelChapter,through='ChapterNewContentEight')
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
        verbose_name=u"是隐藏",
        null=True,
        blank=True)

    class Meta:
        index_together = [
            ["ishide"],
        ]
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name

class ChapterNewContentEight(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelNewContentEight,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    isdel = models.BooleanField(default=False, verbose_name=u"是否删除", null=True, blank=True)

    class Meta:
        index_together = [
            ["isdel"],
        ]
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]


class NovelNewContentNine(models.Model):
    comefrom = models.ForeignKey(
        NovelContentComefrom,
        on_delete=models.SET_NULL,
        to_field='comefrom_id',
        verbose_name=u"小说来源",
        default='', null=True,
        blank=True)
    content = models.TextField(verbose_name=u"小说内容")
    chapter = models.ManyToManyField(NovelChapter,through='ChapterNewContentNine')
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
        verbose_name=u"是隐藏",
        null=True,
        blank=True)

    class Meta:
        index_together = [
            ["ishide"],
        ]
        verbose_name = u"小说内容"
        verbose_name_plural = verbose_name

class ChapterNewContentNine(models.Model):
    novelchapter = models.ForeignKey(NovelChapter,on_delete=models.CASCADE, to_field='chapter_url_md5',verbose_name=u"章节内")
    novelcontent = models.ForeignKey(NovelNewContentNine,on_delete=models.CASCADE, to_field='content_url_md5',verbose_name=u"章节内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    isdel = models.BooleanField(default=False, verbose_name=u"是否删除", null=True, blank=True)

    class Meta:
        index_together = [
            ["isdel"],
        ]
        unique_together = [
            ('novelchapter', 'novelcontent')
        ]
