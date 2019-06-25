from datetime import datetime
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext as _

from project_management.non_project_task.views import __saveNonProjectTask__, \
    __getLoginData__, __privilegeCheck__
#from project_management.projects.fileform import FileUploadForm
from project_management.projects.ProgTaskListsViews import program_task_update
from project_management.Utility import getUserTypeFilter

DEFAULT_DATE = datetime.strptime( '2000-01-01', "%Y-%m-%d" ).date()
USERTYPE = ['Internal', 'External']
THOUSAND = 1000

ACTION_MESSAGE = {'Default':'',
                '':'',
                'TaskExists'    : _('Task Name already exists.'),
                'TaskShared'    : _('Task shared'),
                'DUPLICATE'     : _('Task Name already exists.'),
                'SAVE'      : _('Task saved successfully'),
                'Save'      : _('Task saved successfully'),
                'Access'        :_('Access Denied'),
                'Access Denied'        :_('Access Denied'),
                'InActiveProgram': _('Program/Project is inactive. Cannot be created / updated'),
                'Create'            : _('Create'),
                'CreateError'       : _('Create unsuccessful'),
                'Update'            : _('Update'),
                'UpdateError'       : _('Update unsuccessful'),
                'FileSizeMsg':_('Maximum file size allowed is %sMb'),
                'MaxFilesize':_('Maximum filesize exceed'),
                'Uploadunsuccessful':_('Invalid File. Cannot be uploaded '),
                'SELECTTASKLIST':_('Select valid tasklist'),
                }

#def GetTasklists(request):
#    json = []
#    alltasklist = []
#    allstages = []
#    program = []
#    projectid = request.GET.get('projectid', '')
#    if projectid == '0':
#        allcontacts = FiveGUser.objects.exclude(cancel
#                        = 1).exclude(status = 0)
#    else:
#        if(projectid != ''):
#            program =  Project.objects.get(pk = projectid)
#    alltasklist = ProjectTasklist.objects.filter(program =
#         program).exclude(cancel = 1).order_by('name')
#    nouser, allExternalUsers = __getTeams__(request, 'External', program, '')
#    internalTeam = program.team.all() if program else []
#    allcontacts =  set(internalTeam) | set(allExternalUsers)
#    allstages = program.milestone.filter(category
#        = Milestone.category_choices[1][1]).order_by('name') if program else []
#    results = []
#    tasklist = []
#    if len(alltasklist)>0:
#        for each in alltasklist:
#            tasklist.append( {'name':each.name, 'id':each.pk} )
#    else:
#        if(projectid != '0'):
#            programaskList = CreateDefaultTaskList(program)
#            tasklist.append({'name':programaskList.name, 'id':programaskList.pk})
#        else:
#            tasklist.append({'name':'None', 'id':'0'})
#    results.append(tasklist)
#    contacts = []
#    if len(allcontacts)>0:
#        for each in allcontacts:
#            contacts.append( {'name':each.name, 'id':each.pk,
#                            'sysuserType':each.sysuserType } )
#    results.append(contacts)
#    stages = []
#    if len(allstages)>0:
#        for each in allstages:
#            stages.append( {'name':each.name, 'id':each.pk} )
#    else:
#        stages.append( {'name':'Select', 'id':'0'} )
#    results.append(stages)
#    json = simplejson.dumps(results)
#    return HttpResponse(json, mimetype='application/javascript')


#def GetTasklistsResources(request):
#    projectid = request.GET.get('projectid','0')
#    taskListIDS = request.GET.get('ids','0')
#    if (taskListIDS == '0' or projectid == '0'):
#        return
#    projectTaskList = ProjectTasklist.objects.get(pk = taskListIDS)
#    programTaskListResources = ProjectTaskListTeam.objects.filter(
#                                    programTasklist = projectTaskList)
#    program =  projectTaskList.program
#    if projectid != '0':
#        internalTeam = program.team.filter(sysuserType = USERTYPE[0])
#        externalTeam = program.team.filter(sysuserType = USERTYPE[1])
#        allcontacts = list(set(internalTeam) | set(externalTeam))
#    else:
#        internalTeam = FiveGUser.objects.filter(sysuserType = USERTYPE[0])
#        externalTeam = FiveGUser.objects.filter(sysuserType = USERTYPE[1])
#    allcontacts = set(internalTeam) | set(externalTeam)
#    if taskListIDS != '0':
#        allcontacts = allcontacts & set(
#            [tasklist.user for tasklist in programTaskListResources])
#    #TODO: since we coud'nt sort the dict below query is done
#    contactsU = FiveGUser.objects.none()
#    for each in allcontacts:
#        contactsU = contactsU | FiveGUser.objects.filter(pk = each.pk)
#    allcontacts = contactsU.order_by('name')
#    contacts = [{'name':each.name, 'id':each.pk,
#            'sysuserType':each.sysuserType} for each in allcontacts]
#    json = simplejson.dumps(contacts)
#    return HttpResponse(json, mimetype='application/javascript')

def CreateMenuTaskSave(request):
    userName, userID, privilege = __getLoginData__(request)
    projectid = request.POST.get('project', '')
    non_project_task = ''
    msg = ''
    if projectid != '' and projectid != '0':
        msg = program_task_update(request, 'MenuTask')
    else:
        if __privilegeCheck__(request, privilege):
            msg = 'Access Denied'
        else:
            msg, non_project_task = __saveNonProjectTask__(request)
    if msg != '' and msg != 'SAVE' and msg != 'Save':
        return CreateMenuTaskView(request, msg, non_project_task)
    else:
        return HttpResponseRedirect('/Baseredirect/')

def CreateMenuTaskSaveAndContinue(request):
    userName, userID, privilege = __getLoginData__(request)
    projectid = request.POST.get('project', '')
    task = ''
    msg = ''
    if projectid != '' and projectid != '0':
        msg = program_task_update(request, 'MenuTask')
    else:
        if __privilegeCheck__(request, privilege):
            msg = 'Access Denied'
        else:
            msg, non_project_task = __saveNonProjectTask__(request)
    return CreateMenuTaskView(request, msg, task)



#def CreateMenuTaskView(request, alertmsg = '', tasktoeditagain = ''):
#    msg = alertmsg
#    stageid = '0'
#    form = FileUploadForm()
#    action = 'Create'
#    downloadpath = ''
#    ext_allUsers = ''
#    ext_selectedUsers = ''
#    stages = []
#    programTaskList = []
#    assignedcontacts = []
#    taskstageid = ''
#    taskallocations = []
#    tasktoedit = tasktoeditagain
#    tasklistid = ''
#    assignedTasks = []
#    progprojuser = ''
#    filesize = (settings.MAX_FILE_SIZE / THOUSAND) / THOUSAND
#    fileSizeMsg = ACTION_MESSAGE['FileSizeMsg'] % filesize
#    logindata = request.session['LoginData']
#    projectid = request.session.get('projectid','')
#    allTaskType = TaskType.objects.all()
#    if projectid != '':
#        stageid = request.session.get('stageID','')
#    allTeam = FiveGUser.objects.exclude(cancel
#        = 1).exclude(status = 0).order_by('name')
#    fiveg_user = logindata['loginFiveGUserID']
#    program = Project.objects.filter(Q(apex_body_owner=fiveg_user) |
#        Q(owner=fiveg_user) | Q(team=fiveg_user)).distinct().exclude(cancel=True)
#
#    if projectid != '':
#        programAtCreate = Project.objects.filter(pk = projectid)
#        allcontacts = []
#        allTaskType = TaskType.objects.all()
#        stages = Milestone.objects.exclude(cancel = 1).order_by('name')
#        programTaskList = ProjectTasklist.objects.filter(program
#            = programAtCreate[0]).exclude(cancel = 1).order_by('name')
#
#        if len(programTaskList)>0:
#            programTaskList = programTaskList
#        else:
#            programaskList = CreateDefaultTaskList(programAtCreate[0])
#            programTaskList = ProjectTasklist.objects.filter(program
#                = programAtCreate[0]).exclude(cancel = 1).order_by('name')
#            tasklistid = programaskList.pk
#    int_allTeam, ext_allTeam = getUserTypeFilter(allTeam)
#    return render_to_response('CreateMenuTask.html', {
#            'taskstageid':taskstageid,
#            'taskallocations':taskallocations,
#            'assignedcontacts':assignedcontacts, 'tasktoedit': tasktoedit,
#            'msg':ACTION_MESSAGE[msg], 'assignedTasks':assignedTasks,
#            'downloadpath':downloadpath, 'allcontacts': int_allTeam,
#            'allstages': stages, 'program':program, 'progprojuser':progprojuser,
#            'form':form, 'fileSizeMsg':fileSizeMsg, 'fileName':'',
#            'stageid':stageid, 'alltasktype':allTaskType,
#            'ext_allcontacts':ext_allTeam,
#            'userRole':logindata['loginUserPrivilege'].pk,
#            'ext_assignedcontacts':ext_selectedUsers, 'tasklistid':tasklistid,
#            'action':action, 'programTaskList':programTaskList,
#            'prog_to_up': [], 'userName':logindata['userName'][0],
#            'projectid':projectid }, context_instance = RequestContext(request))
