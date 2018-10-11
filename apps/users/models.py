import os
import uuid
import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from novels import models as novels_models

# Create your models here.
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    sub_folder = 'file'
    if ext.lower() in ["jpg", "png", "gif","bmp","jpeg"]:
        sub_folder = "avatar"
    if ext.lower() in ["pdf", "docx"]:
        sub_folder = "document"
    return os.path.join(str(instance.id), sub_folder, filename)


class UserProfile(AbstractUser):
    old_password= models.CharField(max_length=200, verbose_name=u"老密码", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male",u"男"),("female","女")), default="male")
    mobile = models.CharField(max_length=11, null=True, blank=True,unique=True,verbose_name=u"手机号码")
    image = models.ImageField(upload_to=user_directory_path,default=u"upload/image/default.png", max_length=300,null=True, blank=True,verbose_name=u"用户头像")
    score = models.IntegerField(default=0, verbose_name=u'积分')
    olduserid = models.IntegerField(default=0, verbose_name=u'老用户ID',null=True, blank=True)


    class Meta:

        #index_together = ('host_id', 'Group')  # 联合索引
        unique_together = [
            ('email')
        ]
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def get_gonggao_count(self):
        return UserMessage.objects.filter(user=0, has_read=False).count()

    def get_fav_count(self):

        return self.novelfavorite_set.all().count()

    def get_unread_message_count(self):

        return UserMessage.objects.filter(user=self.id,has_read = False).count()

    def get_grade(self):
        r = '未知'
        for item in settings.USER_LEVEL:
            if item['min'] <= self.score <= item['max']:
                r= item['level']
                break

        return r

    def get_piao_count(self):
        r = 2
        for item in settings.USER_LEVEL:
            if item['min'] <= self.score < item['max']:
                r= item['piao']
                break

        return r

    get_grade.short_description = "等级"
    get_piao_count.short_description = "投票数"

    def __str__(self):
        return self.username

class UserQiandao(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u"签到用户")
    qiandao_time = models.DateTimeField(default=datetime.date.today, verbose_name=u"签到时间")

class UserAsk(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE, verbose_name=u"提问用户")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    comefrom = models.CharField(max_length=500, verbose_name=u"来路" ,default='')
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    create_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u"添加时间")


    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name


    def __str__(self):
        return '用户({0})'.format(self.user.username)


class UserMessage(models.Model):
    user = models.IntegerField(verbose_name=u"接收用户")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    create_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=60, verbose_name=u"验证码")
    email = models.EmailField(max_length=100, verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证码类型", choices=(("register",u"注册"),("forget",u"找回密码"), ("update_email",u"修改邮箱")), max_length=30)
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.datetime.now)
    is_used = models.BooleanField(default=False, verbose_name=u"是否已经使用")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Links(models.Model):
    name = models.CharField(max_length=60, verbose_name=u"名称")
    url = models.CharField(max_length=60, verbose_name=u"网站地址")
    linkid = models.PositiveSmallIntegerField(default=0, verbose_name=u"排序", unique=True)
    ishide = models.BooleanField(default=False,verbose_name=u"是否隐藏")

    class Meta:
        verbose_name = u"友情链接"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}'.format(self.name)