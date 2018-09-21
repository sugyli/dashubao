import os
import uuid
from datetime import datetime

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
    image = models.ImageField(upload_to=user_directory_path,default=u"static/upload/image/default.png", max_length=300,null=True, blank=True,verbose_name=u"用户头像")
    score = models.IntegerField(default=0, verbose_name=u'积分')
    isolduser = models.BooleanField(default=False, verbose_name=u"是否老用户")


    class Meta:

        #index_together = ('host_id', 'Group')  # 联合索引
        unique_together = [
            ('email')
        ]
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def get_grade(self):
        r = '未知'
        for item in settings.USER_LEVEL:
            if item['min'] <= self.score <= item['max']:
                r= item['level']
                break

        return r

    def get_collect(self):
        r = 20

        for item in settings.USER_LEVEL:
            if item['min'] <= self.score <= item['max']:
                r= item['collect']
                break

        return r

    get_grade.short_description = "等级"
    get_collect.short_description = "收藏量"

    def __str__(self):
        return self.username




