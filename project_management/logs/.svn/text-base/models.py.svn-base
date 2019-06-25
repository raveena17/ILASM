from django.db import models

class AuditLog (models.Model):
    timeStamp = models.DateTimeField(auto_now_add = True)
    client = models.CharField(max_length = 120, null = True, blank = True)
    users = models.CharField(max_length = 120, null = True, blank = True)
    screen = models.CharField(max_length = 50, null = True, blank = True)
    actionPerformed = models.CharField(max_length = 50, null = True, blank = True)
    notes = models.TextField(null = True,  blank = True)

    def __unicode__(self):
        return unicode(self.timeStamp)

class SecurityLog (models.Model):
    timeStamp = models.DateTimeField(auto_now_add = True)
    client = models.CharField(max_length = 120, null = True, blank = True)
    users = models.CharField(max_length = 120, null = True, blank = True)
    screen = models.CharField(max_length = 50, null = True, blank = True)
    actionPerformed = models.CharField(max_length = 50, null = True, blank = True)
    notes = models.TextField(null = True,  blank = True)

    def __unicode__(self):
        return unicode(self.timeStamp)

class EventLog (models.Model):
    timeStamp = models.DateTimeField(auto_now_add = True)
    client = models.CharField(max_length = 120, null = True, blank = True)
    users = models.CharField(max_length = 120, null = True, blank = True)
    screen = models.CharField(max_length = 50, null = True, blank = True)
    actionPerformed = models.CharField(max_length = 50, null = True, blank = True)
    notes = models.TextField(null = True,  blank = True)

    def __unicode__(self):
        return unicode(self.timeStamp)

class ErrorLog (models.Model):
    timeStamp = models.DateTimeField(auto_now_add = True)
    client = models.CharField(max_length = 120, null = True, blank = True)
    users = models.CharField(max_length = 120, null = True, blank = True)
    screen = models.CharField(max_length = 50, null = True, blank = True)
    actionPerformed = models.CharField(max_length = 50, null = True, blank = True)
    notes = models.TextField(null = True,  blank = True)

    def __unicode__(self):
        return unicode(self.timeStamp)
