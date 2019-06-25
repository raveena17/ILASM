from django.conf import settings
from django.contrib.sites.models import Site
import socket
import sys


def get_full_domain():
    host = socket.gethostname()
    scheme = 'https'
    if not settings.SECURE_SSL_REDIRECT:
        scheme = 'http'
    return '%s://%s' % (scheme, sys.argv[-1])
