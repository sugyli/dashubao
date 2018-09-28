# -*- coding: utf-8 -*-
__author__ = 'bobby'
__date__ = '2016/10/30 22:11'
from random import Random
#import logging
#from django.core.mail import send_mail

#from django.shortcuts import reverse
from django.conf import settings

from asynchronous_send_mail import send_mail
from users.models import EmailVerifyRecord
#from shubao.settings import EMAIL_FROM,EMAIL_WEB_URL

#logger = logging.getLogger(__name__)

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="forget"):

    if send_type == "update_email":
        code = random_str(6)
    else:
        code = random_str(32)

    kwargs = {
        'code': code,
        'is_used': 0
    }
    if EmailVerifyRecord.objects.filter(**kwargs):
         send_register_email(email, send_type)

    email_record = EmailVerifyRecord()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == "register":
        email_title = "网注册激活链接"
        #url = reverse('novels_info', args=[self.novel_old_id])
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(
                code)

        #send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

    elif send_type == "forget":
        email_title = "注册密码重置链接"
        email_body = "请点击链接修改密码  {0}/users/reset/{1}/".format(settings.EMAIL_V_URL,code)
        send_mail(email_title, email_body, settings.EMAIL_FROM, [email])

    elif send_type == "update_email":
        email_title = "邮箱修改验证码"
        email_body = "你的邮箱验证码为: {0}".format(code)

        #send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

    return True


