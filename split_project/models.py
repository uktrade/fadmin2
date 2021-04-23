from django.db import models

from core.metamodels import BaseModel
from core.models import FinancialYear

from forecast.models import FinancialCode, FinancialPeriod

from previous_years.models import ArchivedFinancialCode


class ProjectSplitCoefficientAbstract(BaseModel):
    financial_period = models.ForeignKey(
        FinancialPeriod,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)ss",
    )
    financial_code_from = models.ForeignKey(
        FinancialCode,
        on_delete=models.PROTECT,
        related_name="from_%(app_label)s_%(class)ss",
    )
    financial_code_to = models.ForeignKey(
        FinancialCode,
        on_delete=models.PROTECT,
        related_name="to_%(app_label)s_%(class)ss",
    )
    split_coefficient = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        abstract = True
        unique_together = (
            "financial_period",
            "financial_code_from",
            "financial_code_to",
        )


class PreviousYearProjectSplitCoefficient(ProjectSplitCoefficientAbstract):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT,)
    financial_code_from = models.ForeignKey(
        ArchivedFinancialCode,
        on_delete=models.PROTECT,
        related_name="from_%(app_label)s_%(class)ss",
    )
    financial_code_to = models.ForeignKey(
        ArchivedFinancialCode,
        on_delete=models.PROTECT,
        related_name="to_%(app_label)s_%(class)ss",
    )

    class Meta:
        unique_together = (
            "financial_year",
            "financial_period",
            "financial_code_from",
            "financial_code_to",
        )


class ProjectSplitCoefficient(ProjectSplitCoefficientAbstract):
    permissions = [
        ("can_upload_files", "Can upload files"),
    ]


class UploadProjectSplitCoefficient(ProjectSplitCoefficientAbstract):
    row_number = models.IntegerField(default=0)
    pass


class TemporaryCalculatedValues(BaseModel):
    # temporary storage for the value calculated.
    financial_code = models.OneToOneField(FinancialCode, on_delete=models.CASCADE,)
    calculated_amount = models.BigIntegerField(null=True, blank=True)
