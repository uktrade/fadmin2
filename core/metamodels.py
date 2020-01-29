from django.db import models

from simple_history.models import HistoricalRecords


class SimpleTimeStampedModel(models.Model):
    """ An abstract base class model that provide self-updating
    'created' and 'modified' field """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimeStampedModel(SimpleTimeStampedModel):
    """ An abstract base class model that provide self-updating
    'created' and 'modified' field, and an active flag"""

    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class LogChangeModel(models.Model):
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class ArchivedModel(models.Model):
    financial_year = models.ForeignKey("core.FinancialYear", on_delete=models.PROTECT)
    archived = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
