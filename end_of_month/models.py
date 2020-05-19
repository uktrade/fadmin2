from django.contrib.auth import get_user_model
from django.db import models

from core.metamodels import BaseModel
from core.models import FinancialYear

from forecast.models import (
    FinancialCode,
    FinancialPeriod,
)


class EndOfMonthStatus(BaseModel):
    archived = models.BooleanField(default=False)
    archived_by = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, blank=True, null=True,
    )
    archived_period = models.OneToOneField(
        FinancialPeriod,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )
    archived_date = models.DateTimeField(blank=True, null=True,)

    class Meta:
        verbose_name = "End of Month Archive Status"
        verbose_name_plural = "End of Month Archive Statuses"
        ordering = ["archived_period"]

    def __str__(self):
        return str(self.archived_period.period_long_name)


class MonthlyTotalBudget(BaseModel):
    # Used to store the budget for each archived month.
    # It could be calculated from the archived budget,
    # but the queries are complex and it is easier to store the total
    amount = models.BigIntegerField(default=0)  # stored in pence
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT,)
    financial_code = models.ForeignKey(
        FinancialCode,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )
    archived_status = models.ForeignKey(
        "end_of_month.EndOfMonthStatus",
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )
    class Meta:
        verbose_name = "Archived total budget"
        verbose_name_plural = "Archived total budget"
        ordering = ["archived_status"]
        unique_together = ("financial_code", "archived_status")
