import logging

from django.db.models import Q

from novels import models as novels_models
from users import models as users_models
from utils import help

logger = logging.getLogger(__name__)

def get_previous_chapter(subsection=False,kwargs={}):
    if not subsection and not 'chapter_type' in kwargs:
        kwargs.update(chapter_type=0)
    kwargs.update(ishide=0)
    return novels_models.NovelChapter.objects.filter(
        **kwargs).order_by("-chapter_order").first()

def get_next_chapter(subsection=False,kwargs={}):
    if not subsection and not 'chapter_type' in kwargs:
        kwargs.update(chapter_type=0)
    kwargs.update(ishide=0)
    return novels_models.NovelChapter.objects.filter(
        **kwargs).order_by("chapter_order").first()

def get_one_chapter(subsection=False,kwargs={}):
    if not subsection and not 'chapter_type' in kwargs:
        kwargs.update(chapter_type=0)
    kwargs.update(ishide=0)
    return novels_models.NovelChapter.objects.filter(
        **kwargs).first()

def get_all_chapter(isdaoxu=None,subsection=False,kwargs={}):
    '''

    :param isdaoxu:
    :param subsection: 是否需要分卷
    :param kwargs:
    :return:
    '''
    if not subsection and not 'chapter_type' in kwargs:
        kwargs.update(chapter_type=0)
    kwargs.update(ishide=0)

    if isdaoxu:
        return novels_models.NovelChapter.objects.filter(
            **kwargs)
    else:
        return novels_models.NovelChapter.objects.filter(
            **kwargs).order_by('-chapter_order')


def get_one_book(kwargs={}):
    return novels_models.NovelDetail.objects.filter(**kwargs, ishide=0).first()


def get_all_book(kwargs={}):
    return novels_models.NovelDetail.objects.filter(**kwargs, ishide=0)





def authenticate(username=None, password=None):
    '''
    验证用户是否存在
    :param self:
    :param username:
    :param password:
    :return:
    '''
    try:
        user = users_models.UserProfile.objects.get(
            Q(username=username) | Q(email=username))

        if len(password) > 0 and (user.check_password(password)
                                  or user.old_password == help.get_md5(password)):
            return user

    except Exception as e:
        logger.debug(e)
        return None

def authuser(username):

    return users_models.UserProfile.objects.filter(Q(username=username) | Q(email=username))

