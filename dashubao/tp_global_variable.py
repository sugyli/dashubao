from django.conf import settings



def read_settings_file(request):
    return {
        'WEB1_NAME': settings.WEB1_NAME,
        'WEB1_URL': settings.WEB1_URL,
        'WAP1_NAME': settings.WAP1_NAME,
        'WAP1_URL': settings.WAP1_URL,
        'DEF_FENMIAN': settings.DEF_FENMIAN
    }