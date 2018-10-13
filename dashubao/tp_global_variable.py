from django.conf import settings
from utils import modelhelp , help


def read_settings_file(request):

    return {
        'WEB1_NAME': settings.WEB1_NAME,
        'WEB1_URL': settings.WEB1_URL,
        'WAP1_NAME': settings.WAP1_NAME,
        'WAP1_URL': settings.WAP1_URL,
        'DEF_FENMIAN': settings.DEF_FENMIAN,
        'FENLEI': modelhelp.get_fenlei(),
        'COME_FROM': help.encryption_urllib_base64(request.path),
        'NOTEXT': settings.NOTEXT
    }