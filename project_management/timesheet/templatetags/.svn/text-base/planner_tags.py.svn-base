"""
    Template tags for the timesheet module.
"""
from django import template
from django.template.defaultfilters import stringfilter

from project_management.tasks.models import Task
from project_management.non_project_task.models import NonProjectTaskAssignees

from datetime import datetime

register = template.Library()

DELIMITER = ':'
FORMAT = '%02d:%02d'
DATE_FORMAT = '%m/%d/%Y'

def get(part):
    default = '00'
    def split(time):
        if DELIMITER in time:
            return time.split(DELIMITER)[part]
        return default
    return split

@register.filter(name = 'get_hour')
@stringfilter
def get_hour(time):
    """
        Returns only the hour from the time string.
    """
    hour_part = 0
    return get(hour_part)(time)

@register.filter(name = 'get_minutes')
@stringfilter
def get_minutes(time):
    """
        Returns only the hour from the time string.
    """
    minutes_part = 1
    return get(minutes_part)(time)

class WorkHoursNode(template.Node):
    """
        Node representing a single time interval.
    """
    def __init__(self, work_hours, var_name):
        self.work_hours = work_hours
        self.var_name = var_name
    def render(self, context):
        try:
            context[self.var_name] = self.work_hours
        except:
            pass
        return ''

@register.tag
def get_work_hours(parser, token):
    """
        Makes a list of work hour intervals
        and sets the value to the specified variable in the context.
    """
    try:
        tokens = token.split_contents()
        if len(tokens) is 4:
            tag_name, intervals, _as, var_name = tokens
        elif len(tokens) is 3 and tokens[1] == 'as':
            tag_name, intervals, var_name = tokens[0], None, tokens[2]
        else:
            raise ValueError
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%r tag requires arguments" % token.contents.split()[0]
    hour_intervals = [0, 30]
    if intervals:
        try:
            hour_intervals = [int(str(i)) for i in intervals.strip('\'"').split(',')]
        except:
            raise template.TemplateSyntaxError, \
                "%r tag had invalid arguments" % tag_name

    hours = range(24)
    work_hours = [ FORMAT % ( hour, mins )
                    for hour in hours for mins in hour_intervals ]
    return WorkHoursNode(work_hours, var_name)


@register.filter(name = 'convert_to_date_object')
@stringfilter
def convert_to_date_object(date_text):
    """ Convert the string date to date object. """
    return datetime.strptime(date_text.strip('/'), DATE_FORMAT).date()


#@register.inclusion_tag('tasklist.html')
#def list_nonproject_tasks(user, num=10):
#    """ Inclusion tag which lists non project tasks. """
#	#    if not user.is_superuser: #admin doesnt contain five user entry
#	#        user = FiveGUser.objects.get(userProfile__authUser = user)
#    return { 'object_list' : Task.objects.filter(project
#        = None).filter(milestone = None).filter(priority = None).filter(status
#        = None)[:num] }
#
#
#@register.inclusion_tag('tasklist.html')
#def list_project_tasks(user, num=10):
#    """ Inclusion tags which project based tasks. """
#
#    return { 'object_list' :  Task.objects.filter(assigned_resources = user)[:num]  }
