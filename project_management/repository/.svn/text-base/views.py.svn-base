"""
    Repository Views
"""
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from project_management.logs.logger import CapturLog
from project_management.repository.fileform import FileUploadForm
from project_management.repository.models import RepositoryTags, Repository
from project_management.Utility import ChangeMode, Util

import os

actionMsg = {
    '': '',
     'Save': _('File Uploaded successfully'),
    'Uploadunsuccessful': _('Invalid File. Cannot be uploaded'),
    'MaxFilesize'           :_('Maximum filesize exceeded'),
    'ProjectInactive': _('Project is inactive. File Upload cannot be done.'),
    'FileSizeMsg':_('Maximum file size allowed is %sMb'),
    'Access Denied': _('Access Denied'),
    }

MODULE = 'repository'
THOUSAND = 1000

def get_program_details(request):
    programId = request.session.get('projectid', '')
    try:
        program = Project.objects.get(id = programId)
    except:
        program = None
    return program



def RepositoryView(request):
    userName = ''
    repositoryTags = RepositoryTags.objects.all()
    repositoryTagID = request.GET.get('tagID', '')
    filesize = (settings.MAX_FILE_SIZE / THOUSAND) / THOUSAND
    fileSizeMsg = actionMsg['FileSizeMsg'] % filesize
    msg = request.GET.get('msg', '')
    LoginData = request.session.get('LoginData', '')
    if LoginData != '':
        userName = LoginData['userName'][0]
    form = FileUploadForm()
    program = get_program_details(request)
    downloadpath = settings.MEDIA_URL
    if repositoryTagID != '':
        repository = Repository.objects.filter(program
            = program).filter(repositoryTag = repositoryTagID)
    else:
        repository = Repository.objects.filter(program = program)
    return render_to_response('Repository.html', {
        'userName': userName, 'downloadpath':downloadpath,
        'prog_to_up': program,'repositoryTags':repositoryTags,
        'msg': actionMsg[msg],'repositoryTagID':repositoryTagID,
        'templateForm': form, 'action': 'Update',
        'repository': repository, 'fileSizeMsg':fileSizeMsg },
        context_instance = RequestContext(request))


def RepositoryUpload(request):
    try:
        form = FileUploadForm(request.POST, request.FILES)
        msg = ''
        flg = 0
        repositoryTag = request.POST.get('repositoryTag', '0')
        if repositoryTag == '':
            repositoryTag = '0'
        if form.is_valid():
            program = get_program_details(request)
            uploadedFile = form.cleaned_data['fileUploaded']
            name = uploadedFile.name
            for each in settings.FILE_EXTENSIONS_TO_EXCLUDE:
                if name.__contains__(each):
                    flg = 1

            if uploadedFile._size > settings.MAX_FILE_SIZE:
                msg = 'MaxFilesize'
                CapturLog().LogData(request, 'Upload', MODULE, actionMsg[msg])
                return RepositoryView(request, msg)

            if flg != 1:
                fileUploaded = request.FILES['fileUploaded']
                check = 0
                ID = request.session.get('projectid', '')
                randomID = Util().Guid()
                repository = Repository.objects.create(fileID
                    = randomID, program_id = ID, repositoryTag_id = repositoryTag)
                filename = fileUploaded.name

                currentdir = settings.MEDIA_ROOT + '/all files/'
                ChangeMode(settings.MEDIA_ROOT)
                ChangeMode(currentdir)
                currentosdir = currentdir
                currentdir = os.listdir(currentdir)
                for each in currentdir:
                    if each == ID:
                        check = 1
                if(check != 1):
                    os.mkdir(currentosdir+ID)

                fd = open('%s/%s' % (currentosdir + ID, randomID + filename), 'wb')
                for chunk in fileUploaded.chunks():
                    fd.write(chunk)
                fd.close()

                filepath = 'all files/' + ID + '/'+randomID + filename if filename !=  '' else ''
                repository.fileUploaded = filepath
                repository.name = name
                repository.save()
                msg = 'Save'
                CapturLog().LogData(request, msg, MODULE, actionMsg[msg], repository)
                form = FileUploadForm()
            else:
                msg = 'Uploadunsuccessful'
                CapturLog().LogData(request, 'Save', MODULE, actionMsg[msg])
        else:
            CapturLog().LogData(request, 'Save', MODULE, actionMsg['Uploadunsuccessful'])
    except (RuntimeError, TypeError, NameError):
        errMessage = ''
        CapturLog().LogData(request, msg, MODULE, actionMsg[msg])

    if request.POST.get('fromHome','') == 'fromHome':
        return HttpResponseRedirect('/ProjectHome/?msg=' + msg)
    else:
        return HttpResponseRedirect('/repository/?msg=' + msg)
