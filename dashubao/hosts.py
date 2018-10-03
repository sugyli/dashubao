from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'm', 'dashubao.mobileurls', name='m'),
    host(r'ww', settings.ROOT_URLCONF, name='ww'),
    host(r'mm', 'dashubao.mobileurls', name='mm'),
)