# Django settings for project_management project.
import os

DEBUG = True
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
# mindshare_jun_20_new,
DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or
        # 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        # Or path to database file if using sqlite3.
        'NAME': 'mindshare_2019',
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '192.168.1.83',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '3306',
    }
}
APPEND_SLASH=False
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/linuxuser/Desktop/projects/Production_ms/Mindshare/project_management/django.log',
            },
        },
    'loggers': {
        'django_cron': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

ALLOWED_HOSTS = ['*']

""" Send a alert mail to admin and reporting senior 
    for probation end date """
ESCALATION_ALERT_FOR_EMPLOYEMENT_STATUS_CHANGE = 'Monday'
EMPLOYEMENT_STATUS_CHANGE_REMINDER_DAYS_LIST = [15,7,1]
EMPLOYEE_STATUS_REMAINDER_FOR_REPORTING_SENIOR = True
EMPLOYEE_STATUS_REMAINDER_FOR_USERS = ['jai.srinivasan@fifthgentech.com','gayathri@5gindia.net']
EMPLOYEE_STATUS_REMAINDER_FOR_ROLES = ['']
# EMPLOYEE_STATUS_REMAINDER_FOR_ROLES = ['Corporate Admin', 'Manager']

"""Short leave applied only two days for a month"""
SHORT_LEAVE_DAYS = 2

""" Send alert mail to hr-desk in leave app"""
REMINDER_FOR_HRDESK=['raveena@5gindia.net']

"""Allowed the year to apply leave"""
CURRENT_YEAR = '2019'

"""Mentioned other leave types without status table"""
OTHER_LEAVE_TYPE=['Compoff','LOP','Maternity']


""" Send a alert mail amc """
AMC_REMINDER_DAYS_LIST = [30,7,1]
AMC_CRON_REMINDER_MAIL_LIST= ['raveena@5gindia.net']
AMC_ADDITIONAL_EMAIL_LIST = ['harshitha@5gindia.net']





# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Asia/Calcutta'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'ta'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

import os.path
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# MEDIA_ROOT = os.path.join(PROJECT_ROOT, "static/")
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, "media")
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static/'),)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "static/files")
MEDIA_URL = '/static/files/'

ADMIN_MEDIA_PREFIX = '/static/'


LOGIN_URL = '/login/'
USER_REDIRECT_URL = '/dashboard/'
# USER_REDIRECT_URL = '/timesheet/'  # 'http://192.168.1.77/trac'#'/timesheet/'
ADMIN_REDIRECT_URL = '/dashboard/'

PAY_IT_STATUS_PATH = os.path.join(MEDIA_ROOT, 'PayITStatus_xl/PayITStatus.xls')

# using  mem catche
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/?timeout=0'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*mf08ik29!*+ed^f7u&px03$*is7+jz@v_o6%y63iu@%u(!9^t'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # must be after session middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.contrib.auth.forms.AuthenticationForm',

)

ROOT_URLCONF = 'project_management.urls'


AUTHENTICATION_BACKENDS = (
    'project_management.access_control.authentication.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
    'project_management.access_control.permission.ObjectPermission',

)

AUTH_PROFILE_MODULE = 'user_profile.UserProfile'

LDAP_SERVER = '192.168.1.102'
LDAP_PASSWORD = "Fivegadmin@2018"

""" Project e-mail related """
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/app-messages'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'raveena@5gindia.net'
EMAIL_HOST_PASSWORD = '17041996'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_MESSAGE_GREE = 'Hello, '
EMAIL_MESSAGE_TXT = 'You have been successfully registered in payit. '
EMAIL_MESSAGE_TXT1 = 'login in to the following url to '
EMAIL_MESSAGE_TXT2 = ''
EMAIL_MESSAGE = EMAIL_MESSAGE_GREE + "\n\t" + EMAIL_MESSAGE_TXT + "\n" + EMAIL_MESSAGE_TXT1 + "\n" +\
    EMAIL_MESSAGE_TXT2 + "\n\t Username = %s \n\t Password = %s "
EMAIL_CONTENT_TYPE = 'html'
MAIL_LOG_FILE = os.path.join(PROJECT_ROOT, 'mail_errorlog.txt')

USER_CREATION_EMAIL_SUBJECT = 'payit registration'
USER_CREATION_EMAIL_MESSAGE = EMAIL_MESSAGE_GREE + "\n\t" + EMAIL_MESSAGE_TXT

NONPROJECT_TASK_ASSIGN_UNASSIGN = 'You have been assigned/unassigned in task %s'

RESET_PWD_EMAIL_MESSAGE = "Welcome,\n\t Your password have been reset successfully.\n\t Username = %s \n\t Password = %s "

FEEDBACK_MESSAGE = "Hello,\n\t You have received a feedback from : %s with E-mail : %s.\n\n\t Rating = %s \n\n\t Comment = %s \n\n\t Suggestion = %s "
##EMAIL_HOST = 'mail.fifthgentech.com'
""" MAX_FILE_SIZE values is in bytes """
MAX_FILE_SIZE = 10000000
FILE_EXTENSIONS_TO_EXCLUDE = ['.exe', '.py', '.sh', '.bat', '.mis', '.dll']
LOGO_PATH = '/css/images'

""" List page setting """
IS_PAGINATION = True
PAGE_SIZE = 10
LOGIN_ATTEMPTS = 5
DASHBOARD_PAGE_SIZE = 5

DATE_FORMAT = 'm-d-Y'
TEMPLATE_COLOR = 'blue'
LIST_DATE_FORMAT = '%b %d, %Y'
TIMESPAN_DATE_FORMAT = '%b %d'

""" Logs to log in the Portal Apps"""
LOG_TEMPLATE = ''  # '/home/username/projects/payit/payit/dataTemplate'
LOG_POST_PATH = ''  # '/home/username/projects/payit/payit'
EVENT_PATH = ''  # '/home/username/projects/payit/payit'

""" setting update configuration """
SETTING_PATH = ''  # '/home/username/projects/payit/payit/apps'
#TEST_RUNNER = 'coverage.test_coverage.coverage_runner.run_tests'

""" PIE Chart Colors """
ON_SCHEDULE = '#8887ff'
AHEAD_SCHEDULE = '#33ff33'
BEHIND_SCHEDULE = '#ff3333'

"""Project Reminder"""
ALERT_ON = 2
ALERT_REMINDER = 2

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #'coverage',
    'pagination',
    'mptt',
    'django_cron',
    'newsletter',
    'announcements',
    'client_visit_report',
    'amc',
    'leave',
    #'memcache_status',
    'project_management.projectbudget',
    'project_management.fields',
    'project_management.logs',
    'project_management.access_control',
    'project_management.address',
    'project_management.alert',
    'project_management.business_unit',
    'project_management.users',
    'project_management.conferenceroombooking',
    'project_management.projects',
    'project_management.notifications',
    'project_management.repository',
    'project_management.non_project_task',
    'project_management.tasks',
    'project_management.common_manager',
    'project_management.timesheet',
    'project_management.timesheetnew',
    'project_management.customer',
    'project_management.milestone',
    'project_management',
    'project_management.management',
    # 'project_management.reimbursement',
    'project_management.travel',
    'new_reimbursement',

    #'project_management.performance_measurement',

    'project_management.code_review',
    'password_change',
    'AMC_Report',
    #'project_management.codereview_matrix',
    # 'rest_framework',

)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, "templates"),
        ],
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                # 'django.core.context_processors.request',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]


try:
    from local_settings import *
except ImportError:
    pass
