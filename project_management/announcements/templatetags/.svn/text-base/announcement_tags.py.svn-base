from django import template
from django.conf import settings
from announcements.models import Announcement

register = template.Library()

announcement_menu_item = '<li><a href="/announcement/view/?ids=%s">%s</a></li>'
announcement_menu_more = '<li><a href="%s">%s</a></li>'

def getLastFiveAnnouncements():
    announcements = Announcement.objects.all()
    announcements = announcements.order_by('-creation_date')[:5]
    announcement_menu = ''
    for each in announcements:
        announcement_menu += announcement_menu_item %(each.pk, each.title[:18])      
    announcement_menu += announcement_menu_more %('/announcement/list/', 'more...')
    return announcement_menu

register.simple_tag(getLastFiveAnnouncements)
