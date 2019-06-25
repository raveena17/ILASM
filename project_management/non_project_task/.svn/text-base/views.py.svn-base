from django.utils.translation import ugettext as _
from django.conf import settings

#from project_management.CommonList import CommonListManager
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
    'DELETEUNSUCCESSFUL' :_('Task is dependent. Cannot be deleted.'),
    'DELETESUCCESSFUL': _('Task deleted successfully'),
    'UPDATEUNSUCCESSFUL' :_('Task status is completed. Cannot be saved.'),
    'List':_('Task listed successfully'),
    'ListErr':_('Task list unsuccessful'),
    'ACCESSDENIED': _('Access Denied')
    }

def __getLoginData__(request):
    userID = ''
    privilege = ''
    LoginData = request.session.get('LoginData','')
    if LoginData != '':
        userName = LoginData['userName'][0]
        userID = LoginData['loginFiveGUserID']
        privilege = LoginData['loginUserPrivilege']
    return userName, userID, privilege

def __privilegeCheck__(request, privilege):
    flag = 0
    if str(privilege) == 'None' or str(privilege) == '0' or str(privilege).strip() == '':
        flag = 1
    return flag

def __getNonProjectTask__(request):
    pretask = NonProjectTask.objects.filter(pk = request.POST.get('taskID', ''))
    if len(pretask)>0:
        userID = pretask[0].owner.pk
    else:
        userName, userID, privilege = __getLoginData__(request)
    non_project_taskData = NonProjectTask(
        pk = request.POST.get('taskID', ''),
        name = request.POST.get('taskName', ''),
        plannedStartDate = GetDateType(request.POST.get('start_date', '')),
        plannedEndDate = GetDateType(request.POST.get('end_date', '')),
        notes = request.POST.get('tasknotes', ''),
        owner_id = userID,
        cancel = 0,
        taskType_id = request.POST.get('taskType', '0')
        )
    return non_project_taskData

def __getNonProjectTaskTeams__(request, non_project_task):
    if len(non_project_task)>0:
        non_project_task = non_project_task[0]
    #allTeam = FiveGUser.objects.exclude(cancel = 1).exclude(status = 0)
    allTeam = User.objects.exclude(cancel = 1).exclude(status = 0)
    non_project_taskTeam =  NonProjectTaskAssignees.objects.filter(
                                non_project_taskID = non_project_task)
    progCont = [team.user for team in non_project_taskTeam]
    teamSet = set(allTeam)
    progContSet = set(progCont)
    diffTeam = teamSet - progContSet
    allTeam = list(diffTeam)
    return allTeam, progCont

def __assignNonProjectTaskTeam__(request, non_project_task):
    userName, userID, privilege = __getLoginData__(request)
    selectedresources = request.POST.getlist('selectedresources') + request.POST.getlist('ext_selectedresources')
    #selectedUser = set([FiveGUser.objects.get(userID = ID)
    selectedUser = set([User.objects.get(id = ID)
                                for ID in selectedresources])
    availableTeam = NonProjectTaskAssignees.objects.filter(non_project_taskID
        = non_project_task.pk)
    availableUser = set([ aTeam.user for aTeam in availableTeam] )
    usersToDel = availableUser - selectedUser
    usersToIns = selectedUser - availableUser
    [NonProjectTaskAssignees(non_project_taskID = non_project_task,
        user = each).save() for each in usersToIns]
    [NonProjectTaskAssignees.objects.filter(non_project_taskID
        = non_project_task).filter(user = delUser).delete()
        for delUser in usersToDel]
    sendingEmail(request, non_project_task)
    return

def __saveTeamDetails__(request, non_project_task):
    availableTeam = NonProjectTaskAssignees.objects.filter(
        non_project_taskID = non_project_task)
    for each in availableTeam:
        start = each.user.pk+'actualstart'
        end = each.user.pk+'actualend'
        status = each.user.pk+'status'
        each.actualstartDate = GetDateType(request.POST.get(start, ''))
        each.actualendDate = GetDateType(request.POST.get(end, ''))
        each.status = request.POST.get(status, 'Incomplete')
        each.save()
    return

#def __saveUserDetails__(request, non_project_task):
#    userName,userID,privilege = __getLoginData__(request)
#    fiveGUser = FiveGUser.objects.filter(pk = userID)[0]
#    availableTeam = NonProjectTaskAssignees.objects.filter(
#        non_project_taskID = non_project_task).filter(user = fiveGUser)
#    for each in availableTeam:
#        start = each.user.pk + 'actualstart'
#        end = each.user.pk + 'actualend'
#        status = each.user.pk + 'status'
#        each.actualstartDate = GetDateType(request.POST.get(start, ''))
#        each.actualendDate = GetDateType(request.POST.get(end, ''))
#        each.status = request.POST.get(status, 'Incomplete')
#        each.save()
#    return

def __saveNonProjectTask__(request):
    msg = ''
    non_project_task = __getNonProjectTask__(request)
    toCheckDuplicate = NonProjectTask.objects.exclude(cancel
        = 1).exclude(pk = non_project_task.pk)
    toCheckDuplicate = toCheckDuplicate.filter(name
                                        = non_project_task.name)
    if len(toCheckDuplicate)>0:
        msg = 'DUPLICATE'
    else:
        non_project_task.save()
        __assignNonProjectTaskTeam__(request, non_project_task)
        if request.POST.get('action', '') == 'Update':
            __saveTeamDetails__(request, non_project_task)
        msg = 'SAVE'
    return msg, non_project_task

#def NonProjectTaskView(request, msg = '', ids = ''):
#    userName = ''
#    privilege = ''
#    loginUser = ''
#    allUsers = ''
#    selectedUsers = ''
#    availableTeam = ''
#    flag = 0
#    action = 'CREATE'
#    userName,userID,privilege = __getLoginData__(request)
#    if (request.GET.get('ids', ids) != ''):
#        ids = request.GET.get('ids', ids)
#    non_project_task = NonProjectTask.objects.filter(pk = ids)
#    if userID:
#        loginUser = FiveGUser.objects.get(pk = userID)
#    allTaskType = TaskType.objects.all()
#    allUsers, selectedUsers = __getNonProjectTaskTeams__(request,
#                                                    non_project_task)
#    if len(non_project_task)>0:
#        availableTeam = NonProjectTaskAssignees.objects.filter(
#                            non_project_taskID = non_project_task[0])
#    try:
#        if (len(non_project_task)>0):
#            non_project_task = non_project_task[0]
#            action = 'UPDATE'
#        if (msg == 'DUPLICATE'):
#            non_project_task = __getNonProjectTask__(request)
#        if __privilegeCheck__(request, privilege) and action == 'CREATE':
#            flag = 1
#        int_allUsers, ext_allUsers = getUserTypeFilter(allUsers)
#        int_selectedUsers, ext_selectedUsers = getUserTypeFilter(selectedUsers)
#    except (RuntimeError, TypeError, NameError):
#            errMessage = ERROR_MESSAGE % (RuntimeError,TypeError,NameError)
#            CapturLog().LogData(request, action+'Error', MODULE, errMessage)
#    if flag == 1:
#        CapturLog().LogData(request, actionMsg[action],
#                                        MODULE, actionMsg['ACCESSDENIED'])
#        return NonProjectTaskList(request, 'ACCESSDENIED')
#    else:
#        CapturLog().LogData(request, actionMsg[action],
#                                                MODULE, actionMsg[action])
#        return render_to_response('CreateNonProgramTask.html',{
#            'title': 'Task', 'action':actionMsg[action],
#            'userName':userName, 'availableTeam':availableTeam,
#            'alltasktype':allTaskType, 'allcontacts':int_allUsers,
#            'assignedcontacts':int_selectedUsers, 'ext_allcontacts':ext_allUsers,
#            'ext_assignedcontacts':ext_selectedUsers,
#            'non_project_task':non_project_task, 'msg':actionMsg[msg],
#            'loginUser':loginUser },
#            context_instance = RequestContext(request))
#
##TODO: to be removed after functiuon is converted in to generic views
#def NonProjectTaskList(response, msg = ''):
#    ACTION = 'List'
#    dataField = []
#    sql = ''
#    userName = ''
#    userID = ''
#    privilege = ''
#    userName, userID, privilege = __getLoginData__(response)
#    displayField = ['S.No', 'Task','Planned Start Date', 'Planned End Date', 'Task Type', 'Status']
#    try:
#        if userID != '0':
#            sql = "select a.non_project_taskID, a.name, a.plannedStartDate, a.plannedEndDate, b.name as TaskType, a.non_project_taskID\
#                from non_project_task_nonprojecttask a, client_profile_tasktype b where a.taskType_id = b.taskTypeid and  ((a.non_project_taskID in (select non_project_taskID_id from non_project_task_nonprojecttaskassignees\
#                where user_id = '"+userID+"')) or a.owner_id = '"+userID+"') and a.cancel<>'1' and a.non_project_taskID <> '0'"
#        else:
#            sql = "select a.non_project_taskID, a.name, a.plannedStartDate, a.plannedEndDate, b.name as TaskType, a.non_project_taskID\
#                from non_project_task_nonprojecttask a, client_profile_tasktype b where a.tasktype_id = b.taskTypeid and a.cancel<>'1' and a.non_project_taskID <> '0'"
#        #dataField = ['non_project_taskID', 'name', 'plannedStartDate', 'plannedEndDate', 'non_project_taskID']
#        comm_Mgr = CommonListManager(None, NonProjectTask, response, 'NonProjectTask', displayField,sql)
#        comm_Mgr.Message(actionMsg[msg])
#        comm_Mgr.MenuLevel(1)
#    except (RuntimeError, TypeError, NameError):
#        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
#        CapturLog().LogData(response, 'ListError', MODULE, actionMsg['ListErr'])
#    else:
#        CapturLog().LogData(response, ACTION, MODULE, actionMsg[ACTION])
#    return comm_Mgr.DisplayList()

def SaveNonProjectTask(request):
    userName, userID, privilege = __getLoginData__(request)
    msg = ''
    non_project_task = ''
    statusmsg = []
    action = request.POST.get('action','')
    try:
        if request.method == 'POST':
            if (action == 'Update'):
                non_project_task = __getNonProjectTask__(request)
                if __privilegeCheck__(request, privilege):
                    msg = 'ACCESSDENIED'
                else:
                    taskallocation = NonProjectTaskAssignees.objects.filter(
                                non_project_taskID = non_project_task.pk)
                    if (len (taskallocation) > 0):
                        for each in taskallocation:
                            if( each.status == 'Complete'):
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
        CapturLog().LogData(request, 'SaveError', MODULE, actionMsg['SaveError'])
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
    action = request.POST.get('action','')
    try:
        if (action == 'Update'):
            non_project_task = __getNonProjectTask__(request)
            if __privilegeCheck__(request, privilege):
                msg = 'ACCESSDENIED'
            else:
                taskallocation = NonProjectTaskAssignees.objects.filter(
                        non_project_taskID = non_project_task.pk)
                if (len (taskallocation) > 0):
                    for each in taskallocation:
                        if( each.status == 'Complete'):
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
        CapturLog().LogData(request, 'SaveError', MODULE, actionMsg['SaveError'])
    else:
        if msg != 'SAVE':
            CapturLog().LogData(request, 'Save', MODULE, actionMsg[msg])
            return NonProjectTaskView(request, msg, non_project_task.pk)
        else:
            CapturLog().LogData(request, 'Save', MODULE, actionMsg[msg],
                                                        non_project_task)
            return NonProjectTaskView(request, msg)
#'''
#def NonProjectTaskDelete(request):
#    userName,userID,privilege = __getLoginData__(request)
#    ACTION = 'Delete'
#    msg = ''
#    tasksToDelete = request.POST.getlist('deleteChecked')
#    try:
#        if __privilegeCheck__(request, privilege):
#            msg = 'ACCESSDENIED'
#        else:
#            for task in tasksToDelete:
#                taskToDel = NonProjectTask.objects.get(pk = task)
#                if taskToDel.owner.pk == userID:
#                    taskallocation = NonProjectTaskAssignees.objects.filter(
#                                                non_project_taskID = taskToDel)
#                    if (len (taskallocation) > 0):
#                        for each in taskallocation:
#                            if( each.status == 'Complete'):
#                                msg = 'DELETEUNSUCCESSFUL'
#                    if msg != 'DELETEUNSUCCESSFUL':
#                        taskToDel.cancel = 1
#                        taskToDel.save()
#                        msg = 'DELETESUCCESSFUL'
#                        CapturLog().LogData(request, ACTION, MODULE,
#                                        actionMsg[msg], taskToDel)
#                else:
#                    msg = 'ACCESSDENIED'
#    except (RuntimeError, TypeError, NameError):
#        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
#        CapturLog().LogData(request, ACTION, MODULE, errMessage)
#    return NonProjectTaskList(request, msg)
#'''

def sendingEmail(request, task):
    """  send email to the members when a non project task is assigned """
    taskallocationusers = NonProjectTaskAssignees.objects.filter(non_project_taskID = task.pk)
    if (len(taskallocationusers) > 0):
        #fivegusers = [FiveGUser.objects.filter(pk = each.user_id)
        fivegusers = [User.objects.filter(pk = each.user_id)
                                for each in taskallocationusers]
        userprofiles = [UserProfile.objects.get(pk = each[0].userProfile_id)
                                        for each in fivegusers]
        users = [User.objects.get(pk = each.authUser_id)
                                        for each in userprofiles]
        email_message = settings.NONPROJECT_TASK_ASSIGN_UNASSIGN % (task.name)
        try:
            for each in users:
                Email().send_email('Assign/Unassign Task', email_message,
                                                    [each.email,], request)
                CapturLog().LogData(request, 'E-Mail', MODULE,
                                                    'mail sent successfull')
        except Exception:
            errMessage = 'Email Sennding failed \n %s' % ( Exception )
            CapturLog().LogData(request, 'E-MailErr', MODULE, errMessage)

