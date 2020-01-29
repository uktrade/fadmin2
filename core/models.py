from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Group,
    Permission,
)
from django.db import models

from simple_history import register

from .metamodels import (
    LogChangeModel,
    TimeStampedModel,
)


class EventLog(TimeStampedModel, LogChangeModel):
    EventType = models.CharField(max_length=500)


class FinancialYear(LogChangeModel):
    """Key and representation of the financial year"""
    financial_year = models.IntegerField(primary_key=True)
    financial_year_display = models.CharField(max_length=20)
    current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.financial_year_display)


class Document(TimeStampedModel, LogChangeModel):
    """Used to test S3 upload"""

    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()


# Track changes to permissions
register(Permission, app=__package__, inherit=True)
register(get_user_model(), app=__package__, inherit=True)
register(Group, app=__package__, inherit=True)
