import os, sys
sys.path.append('/opt/Mindshare/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project_management.settings'
import django.core.handlers.wsgi
django.setup()
sys.stdout = sys.__stdout__
sys.stdin = sys.__stdin__
application = django.core.handlers.wsgi.WSGIHandler()

