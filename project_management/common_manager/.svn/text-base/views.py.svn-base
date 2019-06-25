"""
    Master Configuration Views
"""
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from project_management.common_manager.master_forms import \
  ProjectTypeForm, RepositoryTagForm, DomainForm,  \
  DevelopmentProcessForm, deleteProjectType, deleteRepositoryTag, deleteDomain, \
  deleteTechnology, delete_development_process, TechnologyForm
from project_management.projects.models import ProjectType, Domain, \
    Technology, DevelopmentProcess
from project_management.repository.models import RepositoryTags
from project_management.common_manager.models import MasterConfig
from project_management.logs.logger import CapturLog
from project_management.Utility import GetLoginUserName

actionMsg = {
    '':'',
    'Duplicate': _('%s name already exists'),
    'Required': _('%s name cannot be empty'),
    'CountryRequired': _('Select country for the %s'),
    'Create':'Create',
    'SelectRecord':_('Select a Record to Delete'),
    'Save':_('%s saved successfully'),
    'Delete_Success':_('%s deleted successfully'),
    'Delete_UnSuccess':_('%s is dependent. Cannot be deleted'),
    'ACCESS_DENIED': _('Access Denied'),
    'SAVESetting':_('Setting saved successfully'),
    'SENDMAIL': _('Test mail sent successfully'),
    'SENDMAILFAIL': _('Test mail sent fail'),
    'APPLYSUC':_('Settings applied successfully.\
                    Please logoff and login in new browser.'),
    'Uploaded':_('Logo uploaded '),
    }

ERROR_MESSAGE = '%s:%s:%s'
MODULE = 'Master'
ACTION = 'List'
MEDIA_PATH = settings.SETTING_PATH + '/' + settings.DATABASE_NAME + '/media/css'

MODEL_FORM = {
          'ProjectTypeForm': ProjectTypeForm,
          'RepositoryTagForm': RepositoryTagForm,
          'DomainForm': DomainForm,
          'TechnologyForm': TechnologyForm,
          'DevelopmentProcessForm':DevelopmentProcessForm,
         }

MODELS = {
          'ProjectTypeForm':ProjectType,
          'RepositoryTagForm':RepositoryTags,
          'DomainForm':Domain,
          'TechnologyForm':Technology,
          'DevelopmentProcessForm':DevelopmentProcess,
         }

DELETE_METHOD = {
          'ProjectTypeForm':deleteProjectType,
          'RepositoryTagForm':deleteRepositoryTag,
          'DomainForm':deleteDomain,
          'TechnologyForm':deleteTechnology,
          'DevelopmentProcessForm': delete_development_process,
          }

#CSS_FILE_NAME = {
#    'blue': 'b_style.css',
#    'green': 'g_style.css',
#    'orange': 'o_style.css',
#    'mpink': 'm_style.css',
#    }

def MasterView (request, dataForm = None, msg = ''):
    """ view to display master configuration """
    userName = ''
    try:
        userName = GetLoginUserName(request)
        masterConfig = MasterConfig.objects.all().order_by('sequenceNo')
        pkID = request.GET.get('ids', '')
        dynamicForm =  request.GET.get('name', 'DomainForm') \
                        if(request.GET.__contains__('name')) else \
                        request.session.get('dynamicForm','DomainForm')
        request.session['dynamicForm'] = dynamicForm
        request.session['pkID'] = pkID
        models = MODELS [dynamicForm]
        masterList, page_range =  getListData(request, models)
        formData =  models.objects.get(pk = pkID) if pkID != '' else models()
        dynamicModelForm =  MODEL_FORM[dynamicForm](instance = formData)
    except (RuntimeError, TypeError, NameError):
        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
        CapturLog().LogData(request, MODULE + 'Error', MODULE, errMessage)
    return render_to_response ('CommonMaster.html', {
        'title': 'Master', 'userName':userName,
        'message':msg, 'page_range': page_range,
        'dynamicForm':dynamicForm,
        'masterConfig':masterConfig, 'formdata':dynamicModelForm,
        'masterList':masterList}, context_instance = RequestContext(request))

def MasterSave(request):
    """ master configuration save """
    dynamicModelForm = request.session.get('dynamicForm','TypeForm')
    msg = action = ''
    if request.method == 'POST':
        dynamicModelForm, msg, action = formSave(request)
    return MasterView(request, dynamicModelForm, msg)

def formSave(request, fromProject = False):
    """ save validation for master config """
    action = ''
    msg = ''
    preData = []
    postData = []
    if fromProject:
        dynamicForm = request.POST.get('formname','TypeForm')
        pkID = request.POST.get('pkID','')
    else:
        dynamicForm = request.POST.get('masterType','DomainForm')
        modelName = dynamicForm.strip('Form')
        pkID = request.session.get('pkID', '')
    try:
        models = MODELS [dynamicForm]
        if pkID != '':
            preData = models.objects.get(pk = pkID)
            formData =  models.objects.get(pk = pkID)
            dynamicModelForm =  MODEL_FORM[dynamicForm](request.POST, instance = formData)
        else:
            dynamicModelForm = MODEL_FORM[dynamicForm](request.POST)

        """ Validation for the forms """
        nameData = dynamicModelForm['name'].data
        duplicateChk = models.objects.filter(name = nameData) if pkID == '' else  models.objects.exclude(pk = pkID).filter(name = nameData)
        if (len(duplicateChk) > 0):
            action = 'Duplicate'

        if(dynamicModelForm['name'].data == ''):
            action = 'Required'

        if dynamicForm == 'StateForm' and (dynamicModelForm['country'].data == ''):
            action = 'CountryRequired'

        if dynamicModelForm.is_valid() and action == '':
            dynamicModelForm.save()
            postData = models.objects.get(name = dynamicModelForm['name'].data)
            action = 'Save'
        msg = actionMsg[action] % modelName

    except (RuntimeError, TypeError, NameError):
        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
        CapturLog().LogData(request, action + 'Error', MODULE, errMessage)
    else:
        if preData == []:
            CapturLog().LogData(request, action, MODULE, msg, postData)
        else:
            CapturLog().LogData(request, action, MODULE, msg, postData, preData)

    return dynamicModelForm, msg, action

def getListData(request, models):
    """ pagination for master config """
    pageNo = request.GET.get('pageNo', '')
    pageNo = 1 if (pageNo == '') else int(pageNo)
    sortCol = request.GET.get('sortCol', '')
    sortCol = '-name' if sortCol != '' and  sortCol == request.session.get('sortCol','') else 'name'
    request.session['sortCol'] = sortCol
    masterList =  models.objects.all().exclude(pk = '0').order_by(sortCol)
    paginator = Paginator(masterList, settings.PAGE_SIZE)
    page_range = paginator.page_range
    if pageNo != 0:
        page_data = paginator.page(int(pageNo))
        masterList = page_data.object_list
    return masterList, page_range


def MasterDelete(request):
    """ delete for master config """
    msg = ''
    action = ''
    try:
        if (request.method == 'POST'):
            masterIDS = request.POST.getlist('deleteChecked')
            dynamicForm = request.POST.get('masterType', 'DomainForm')
            modelName = dynamicForm.strip('Form')
            action =  'Delete_Success' if len (DELETE_METHOD[dynamicForm](masterIDS)) > 0 else 'Delete_UnSuccess' \
                                        if (masterIDS != []) else 'SelectRecord'
            msg = actionMsg[action] if (action== 'SelectRecord') else actionMsg[action] % modelName
    except (RuntimeError, TypeError, NameError):
        errMessage = ERROR_MESSAGE % (RuntimeError, TypeError, NameError)
        CapturLog().LogData(request, action, MODULE, errMessage)
    finally:
        return MasterView(request, dynamicForm, msg)

## also used for domain and technology
#def CreateTagOrProjectTypeFromProject(request):
#    """ to create project type, domain """
#    userName = GetLoginUserName(request)
#    program = ProgramContentDetails(request)
#    formName = request.GET.get('name', 'TypeForm')
#    title = formName.strip('Form')
#    projectID = request.GET.get('ids', '')
#    pkID = request.GET.get('pkID', '')
#    models = MODELS [formName]
#    formData =  models.objects.get(pk = pkID) if pkID != '' else models()
#    dynamicModelForm =  MODEL_FORM[formName](instance = formData)
#    return render_to_response('Create_Tag_Or_ProjectType.html', {
#        'userName':userName, 'projectID':projectID,
#        'prog_to_up': program,
#        'title':title, 'dynamicModelForm':dynamicModelForm,
#        'formName':formName, 'pkID':pkID },
#        context_instance = RequestContext(request))
#
## also used for domain
#def SaveTagOrProjectTypeFromProject(request):
#    """ to save project type, domain """
#    userName = GetLoginUserName(request)
#    project = request.POST.get('projectID', '')
#    dynamicModelForm, msg, action  = formSave(request, True)
#    program = ProgramContentDetails(request)
#    formName = request.POST.get('formname', 'TypeForm')
#    title = formName.strip('Form')
#    message = actionMsg[action] % title
#    if action == 'Save':
#        return HttpResponseRedirect('/project/initiation/?msg=' + message) \
#            if project.strip('') == '' else \
#            HttpResponseRedirect('/project/update/?ids='+project+'&msg='+message)
#    else:
#        pkID = request.POST.get('pkID', '')
#        return render_to_response('Create_Tag_Or_ProjectType.html', {
#            'userName':userName, 'projectID':project,
#            'prog_to_up': program,
#            'title':title, 'dynamicModelForm':dynamicModelForm,
#            'formName':formName, 'pkID':pkID, 'message': message},
#            context_instance = RequestContext(request))
