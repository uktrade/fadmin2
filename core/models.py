from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Group,
    Permission,
)
from django.db import models

from simple_history import register

from .metamodels import (
    BaseModel,
    IsActiveModel,
)


class EventLog(IsActiveModel):
    EventType = models.CharField(max_length=500)


class FinancialYear(BaseModel):
    """Key and representation of the financial year"""
    financial_year = models.IntegerField(primary_key=True)
    financial_year_display = models.CharField(max_length=20)
    current = models.BooleanField(default=False)
    data_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.financial_year_display)


# Track changes to permissions
register(Permission, app=__package__, inherit=True)
register(get_user_model(), app=__package__, inherit=True)
register(Group, app=__package__, inherit=True)
