from django.conf import settings

from project_management.logs.models import AuditLog, SecurityLog, \
    EventLog, ErrorLog

import os


ACTION = ['Create', 'Update', 'Delete', 'List', 'E-Mail']
ERR_ACTION = ['CreateError', 'UpdateError', 'DeleteError', 'ListError',
                'E-MailError', 'CreateErr', 'UpdateErr', 'DeleteErr',
                'ListErr', 'E-MailErr']
SEC_MSG = ['Access Denied', 'LoginError']
NOT_TO_LOG_ACTION = ['List', 'LoginError', 'View']
NOT_TO_LOG_MESSAGE = ['Create', 'Update', 'Delete', 'Access Denied']

LOG_TYPE_TEMPLATE = {'auditLog':'/auditLogT.py',
                    'errorLog':'/errorLogT.py',
                    'eventLog':'/eventLogT.py',
                    'securityLog':'/securityLogT.py'}

class CapturLog(object):

    def __init__(self):
        self.user = None
        self.client = None
        self.screen = None

    def LogData (self, response, action, screen, message, postData = None, preData = None):
        LoginData = response.session.get('LoginData', '')
        if LoginData != '':
            self.user = LoginData['loginUserName']
            self.client = LoginData['clientName']
        if(message == None or self.user == None or self.user == ''):
            return
        self.screen = screen
        #Event Log
        if(action not in NOT_TO_LOG_ACTION and message not in NOT_TO_LOG_MESSAGE):
            self.__eventLog__(action, message)

        if(preData or postData):
            postDataString = self.__getDataString__(postData.__dict__)  if (postData != None) else ''
            preDataString = self.__getDataString__(preData.__dict__)  if (preData != None) else ''

            self.__auditLog__(action, preDataString, postDataString)
            #self.__eventLog__(action,message)
        else:
            #self.__eventLog__(action, message)
            if(message in SEC_MSG or action in SEC_MSG):
                self.__securityLog__(action, message)
            if (action in ERR_ACTION):
                self.__errorLog__(action, message)

    def __getDataString__(self, dict):
        str = '%s : %s,'
        strVal = ''
        for keys in dict:
            strVal = strVal + str % (keys, dict[keys])
        return strVal

    def __auditLog__(self, action, postData, preData):
        auditData = 'AfterUpdate:%s BeforeUpdate:%s'
        auditData = auditData % (preData, postData)

        auditLog = AuditLog(client = self.client,
                    users = self.user,
                    screen = self.screen,
                    actionPerformed = action,
                    notes = auditData)
        auditLog.save()
        self.__postLog__('auditLog', auditLog)

    def __eventLog__(self, action, message):
        eventLog = EventLog(client = self.client,
                    users = self.user,
                    screen = self.screen,
                    actionPerformed = action,
                    notes = message)
        eventLog.save()
        self.__postLog__('eventLog', eventLog)

    def __securityLog__(self, action, message):
        securityLog = SecurityLog(client = self.client,
                    users = self.user,
                    screen = self.screen,
                    actionPerformed = action,
                    notes = message)
        securityLog.save()
        self.__postLog__('securityLog', securityLog)

    def __errorLog__(self, action, message):
        errorLog = ErrorLog(client = self.client,
                    users = self.user,
                    screen = self.screen,
                    actionPerformed = action,
                    notes = message)
        errorLog.save()
        self.__postLog__('errorLog', errorLog)

    def __postLog__(self, logType, logData):
        try:
            logFile = LOG_TYPE_TEMPLATE[logType]
            readLogData = open(settings.LOG_TEMPLATE + logFile)
            logDataFormat = readLogData.read()
            readLogData.close()
            logDataFormat = logDataFormat % (logData.client, logData.users, logData.screen, \
                                            logData.actionPerformed, logData.notes)
            postPath = settings.LOG_POST_PATH
            __chmd__(postPath, logFile.strip('/'))
            postLogFile = postPath + logFile
            if(os.access(postLogFile, os.W_OK)):
                postLogData = open(postLogFile, "w")
                postLogData.write(unicode(logDataFormat).encode('utf-8'))
                postLogData.close()
                os.system("cd " + postPath + "; sudopython " + logFile.strip('/'))
        finally:
            return

def __chmd__(dirname, name):
    dirmode = 755
    flmode = 755
    name = os.path.join(dirname, name)
    if os.path.isdir(dirname):
        os.system('chmod %d "%s"' % (dirmode, dirname))
        # os.chmod(fl, dirmode)   # <--- Does not work
    if os.path.isfile(name):
        os.system('chmod %d "%s"' % (flmode, name))
        # os.chmod(fl, flmode)    # <--- Does not work

if __name__ == '__main__':
    tLog = CaptureLog()
