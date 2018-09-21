from django.db.models import Q

from novels import models as novels_models


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

