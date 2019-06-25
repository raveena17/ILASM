from django.utils.translation import ugettext as _
from django.conf import settings
from project_management.logs.logger import CapturLog
from project_management.non_project_task.models import NonProjectTask, \
    NonProjectTaskAssignees
#from project_management.users.models import FiveGUser
from project_management.Utility import GetDateType, Email
from project_management.users.models import UserProfile

ERROR_MESSAGE = '%s:%s:%s'
MODULE = 'NonProjectTask'
ACTION = 'List'
errMessage = ''
msg = ''

actionMsg = {
    '': '',
    'DUPLICATE': _('Task name already exists'),
    'CREATE': _('Create'),
    'UPDATE': _('Update'),
    'SAVE': _('Task saved successfully'),
    'DELETEUNSUCCESSFUL': _('Task is dependent. Cannot be deleted.'),
    'DELETESUCCESSFUL': _('Task deleted successfully'),
    'UPDATEUNSUCCESSFUL': _('Task status is completed. Cannot be saved.'),
    'List': _('Task listed successfully'),
    'ListErr': _('Task list unsuccessful'),
    'ACCESSDENIED': _('Access Denied')
}


def __getLoginData__(request):
    userID = ''
    privilege = ''
    LoginData = request.session.get('LoginData', '')
    if LoginData != '':
        userName = LoginData['userName'][0]
        userID = LoginData['loginFiveGUserID']
        privilege = LoginData['loginUserPrivilege']
    return userName, userID, privilege

def __privilegeCheck__(request, privilege):
    flag = 0
    if str(privilege) == 'None' or str(
            privilege) == '0' or str(privilege).strip() == '':
        flag = 1
    return flag

def __getNonProjectTask__(request):
    pretask = NonProjectTask.objects.filter(pk=request.POST.get('taskID', ''))
    if len(pretask) > 0:
        userID = pretask[0].owner.pk
    else:
        userName, userID, privilege = __getLoginData__(request)
    non_project_taskData = NonProjectTask(
        pk=request.POST.get('taskID', ''),
        name=request.POST.get('taskName', ''),
        plannedStartDate=GetDateType(request.POST.get('start_date', '')),
        plannedEndDate=GetDateType(request.POST.get('end_date', '')),
        notes=request.POST.get('tasknotes', ''),
        owner_id=userID,
        cancel=0,
        taskType_id=request.POST.get('taskType', '0')
    )
    return non_project_taskData

def __getNonProjectTaskTeams__(request, non_project_task):
    if len(non_project_task) > 0:
        non_project_task = non_project_task[0]
    #allTeam = FiveGUser.objects.exclude(cancel = 1).exclude(status = 0)
    allTeam = User.objects.exclude(cancel=1).exclude(status=0)
    non_project_taskTeam = NonProjectTaskAssignees.objects.filter(
        non_project_taskID=non_project_task)
    progCont = [team.user for team in non_project_taskTeam]
    teamSet = set(allTeam)
    progContSet = set(progCont)
    diffTeam = teamSet - progContSet
    allTeam = list(diffTeam)
    return allTeam, progCont

def __assignNonProjectTaskTeam__(request, non_project_task):
    userName, userID, privilege = __getLoginData__(request)
    selectedresources = request.POST.getlist(
        'selectedresources') + request.POST.getlist('ext_selectedresources')
    # selectedUser = set([FiveGUser.objects.get(userID = ID)
    selectedUser = set([User.objects.get(id=ID)
                        for ID in selectedresources])
    availableTeam = NonProjectTaskAssignees.objects.filter(
        non_project_taskID=non_project_task.pk)
    availableUser = set([aTeam.user for aTeam in availableTeam])
    usersToDel = availableUser - selectedUser
    usersToIns = selectedUser - availableUser
    [NonProjectTaskAssignees(non_project_taskID=non_project_task,
                             user=each).save() for each in usersToIns]
    [NonProjectTaskAssignees.objects.filter(non_project_taskID=non_project_task).filter(
        user=delUser).delete() for delUser in usersToDel]
    sendingEmail(request, non_project_task)
    return

def __saveTeamDetails__(request, non_project_task):
    availableTeam = NonProjectTaskAssignees.objects.filter(
        non_project_taskID=non_project_task)
    for each in availableTeam:
        start = each.user.pk + 'actualstart'
        end = each.user.pk + 'actualend'
        status = each.user.pk + 'status'
        each.actualstartDate = GetDateType(request.POST.get(start, ''))
        each.actualendDate = GetDateType(request.POST.get(end, ''))
        each.status = request.POST.get(status, 'Incomplete')
        each.save()
    return

def __saveNonProjectTask__(request):
    msg = ''
    non_project_task = __getNonProjectTask__(request)
    toCheckDuplicate = NonProjectTask.objects.exclude(
        cancel=1).exclude(pk=non_project_task.pk)
    toCheckDuplicate = toCheckDuplicate.filter(name=non_project_task.name)
    if len(toCheckDuplicate) > 0:
        msg = 'DUPLICATE'
    else:
        non_project_task.save()
        __assignNonProjectTaskTeam__(request, non_project_task)
        if request.POST.get('action', '') == 'Update':
            __saveTeamDetails__(request, non_project_task)
        msg = 'SAVE'
    return msg, non_project_task

def SaveNonProjectTask(request):
    userName, userID, privilege = __getLoginData__(request)
    msg = ''
    non_project_task = ''
    statusmsg = []
    action = request.POST.get('action', '')
    try:
        if request.method == 'POST':
            if (action == 'Update'):
                non_project_task = __getNonProjectTask__(request)
                if __privilegeCheck__(request, privilege):
                    msg = 'ACCESSDENIED'
                else:
                    taskallocation = NonProjectTaskAssignees.objects.filter(
                        non_project_taskID=non_project_task.pk)
                    if (len(taskallocation) > 0):
                        for each in taskallocation:
                            if(each.status == 'Complete'):
                                statusmsg.append('UPDATEUNSUCCESSFUL')
                            else:
                                statusmsg.append('SAVE')
                    if statusmsg != [] and not statusmsg.__contains__('SAVE'):
                        msg = 'UPDATEUNSUCCESSFUL'
                    if msg != 'UPDATEUNSUCCESSFUL':
                        if non_project_task.owner.pk == userID:
                            msg, non_project_task = __saveNonProjectTask__(
                                request)
                        else:
                            __saveUserDetails__(request, non_project_task)
                            msg = 'SAVE'
            else:
                msg, non_project_task = __saveNonProjectTask__(request)
    except (RuntimeError, TypeError, NameError):
        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
        CapturLog().LogData(
            request,
            'SaveError',
            MODULE,
            actionMsg['SaveError'])
    else:
        if msg != 'SAVE':
            CapturLog().LogData(request, 'Save', MODULE, actionMsg[msg])
            return NonProjectTaskView(request, msg, non_project_task.pk)
        else:
            CapturLog().LogData(request, 'Save', MODULE, actionMsg[msg],
                                non_project_task)
            return NonProjectTaskList(request, msg)

def SaveAndContinueNonProjectTask(request):
    userName, userID, privilege = __getLoginData__(request)
    msg = ''
    statusmsg = []
    non_project_task = ''
    action = request.POST.get('action', '')
    try:
        if (action == 'Update'):
            non_project_task = __getNonProjectTask__(request)
            if __privilegeCheck__(request, privilege):
                msg = 'ACCESSDENIED'
            else:
                taskallocation = NonProjectTaskAssignees.objects.filter(
                    non_project_taskID=non_project_task.pk)
                if (len(taskallocation) > 0):
                    for each in taskallocation:
                        if(each.status == 'Complete'):
                            statusmsg.append('UPDATEUNSUCCESSFUL')
                        else:
                            statusmsg.append('SAVE')
                if statusmsg != [] and not statusmsg.__contains__('SAVE'):
                    msg = 'UPDATEUNSUCCESSFUL'
                if msg != 'UPDATEUNSUCCESSFUL':
                    if non_project_task.owner.pk == userID:
                        msg, non_project_task = __saveNonProjectTask__(request)
                    else:
                        __saveUserDetails__(request, non_project_task)
                        msg = 'SAVE'
        else:
            msg, non_project_task = __saveNonProjectTask__(request)
    except (RuntimeError, TypeError, NameError):
        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
        CapturLog().LogData(
            request,
            'SaveError',
            MODULE,
            actionMsg['SaveError'])
    else:
        if msg != 'SAVE':
            CapturLog().LogData(request, 'Save', MODULE, actionMsg[msg])
            return NonProjectTaskView(request, msg, non_project_task.pk)
        else:
            CapturLog().LogData(request, 'Save', MODULE, actionMsg[msg],
                                non_project_task)
            return NonProjectTaskView(request, msg)

def sendingEmail(request, task):
    """  send email to the members when a non project task is assigned """
    taskallocationusers = NonProjectTaskAssignees.objects.filter(
        non_project_taskID=task.pk)
    if (len(taskallocationusers) > 0):
        # fivegusers = [FiveGUser.objects.filter(pk = each.user_id)
        fivegusers = [User.objects.filter(pk=each.user_id)
                      for each in taskallocationusers]
        userprofiles = [UserProfile.objects.get(pk=each[0].userProfile_id)
                        for each in fivegusers]
        users = [User.objects.get(pk=each.authUser_id)
                 for each in userprofiles]
        email_message = settings.NONPROJECT_TASK_ASSIGN_UNASSIGN % (task.name)
        try:
            for each in users:
                Email().send_email('Assign/Unassign Task', email_message,
                                   [each.email, ], request)
                CapturLog().LogData(request, 'E-Mail', MODULE,
                                    'mail sent successfull')
        except Exception:
            errMessage = 'Email Sennding failed \n %s' % (Exception)
            CapturLog().LogData(request, 'E-MailErr', MODULE, errMessage)
