"""
    Master Configuration models
"""
from django.db import models

class MasterConfig (models.Model):
    """
        model for master configuration
    """
    name = models.CharField(max_length = 50)
    formName = models.CharField(max_length = 50)
    sequenceNo = models.IntegerField()

    def __unicode__(self):
        return self.name

