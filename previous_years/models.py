from django.db import models
from django.db.models import (
    Q,
    UniqueConstraint,
)

from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
)

from core.metamodels import (
    ArchivedModel,
)
from core.models import FinancialYear

from costcentre.models import HistoricCostCentre

from forecast.models import (
    DisplaySubTotalManager,
    ForecastExpenditureType,
)


class ArchivedFinancialCode(ArchivedModel):
    """Contains the members of Chart of Account needed to create a unique key"""

    class Meta:
        # Several constraints required, to cover all the permutations of
        # fields that can be Null
        constraints = [
            UniqueConstraint(
                fields=[
                    "archived_programme",
                    "archived_cost_centre",
                    "archived_natural_account_code",
                    "archived_analysis1_code",
                    "archived_analysis2_code",
                    "archived_project_code",
                ],
                name="archived_financial_row_unique_6",
                condition=Q(archived_analysis1_code__isnull=False)
                & Q(archived_analysis2_code__isnull=False)
                & Q(archived_project_code__isnull=False),
            ),
            UniqueConstraint(
                fields=[
                    "archived_programme",
                    "archived_cost_centre",
                    "archived_natural_account_code",
                    "archived_analysis2_code",
                    "archived_project_code",
                ],
                name="archived_financial_row_unique_5a",
                condition=Q(archived_analysis1_code__isnull=True)
                & Q(archived_analysis2_code__isnull=False)
                & Q(archived_project_code__isnull=False),
            ),
            UniqueConstraint(
                fields=[
                    "archived_programme",
                    "archived_cost_centre",
                    "archived_natural_account_code",
                    "archived_analysis1_code",
                    "archived_project_code",
                ],
                name="archived_financial_row_unique_5b",
                condition=Q(archived_analysis1_code__isnull=False)
                & Q(archived_analysis2_code__isnull=True)
                & Q(archived_project_code__isnull=False),
            ),
            UniqueConstraint(
                fields=[
                    "archived_programme",
                    "archived_cost_centre",
                    "archived_natural_account_code",
                    "archived_analysis1_code",
                    "archived_analysis2_code",
                ],
                name="archived_financial_row_unique_5c",
                condition=Q(archived_analysis1_code__isnull=False)
                & Q(archived_analysis2_code__isnull=False)
                & Q(archived_project_code__isnull=True),
            ),
            UniqueConstraint(
                fields=[
                    "archived_programme",
                    "archived_cost_centre",
                    "archived_natural_account_code",
                    "archived_project_code",
                ],
                name="archived_financial_row_unique_4a",
                condition=Q(archived_analysis1_code__isnull=True)
                & Q(archived_analysis2_code__isnull=True)
                & Q(archived_project_code__isnull=False),
            ),
            UniqueConstraint(
                fields=[
                    "archived_programme",
                    "archived_cost_centre",
                    "archived_natural_account_code",
                    "archived_analysis1_code",
                ],
                name="archived_financial_row_unique_4b",
                condition=Q(archived_analysis1_code__isnull=False)
                & Q(archived_analysis2_code__isnull=True)
                & Q(archived_project_code__isnull=True),
            ),
            UniqueConstraint(
                fields=[
                    "archived_programme",
                    "archived_cost_centre",
                    "archived_natural_account_code",
                    "archived_analysis2_code",
                ],
                name="archived_financial_row_unique_4c",
                condition=Q(archived_analysis1_code__isnull=True)
                & Q(archived_analysis2_code__isnull=False)
                & Q(archived_project_code__isnull=True),
            ),
            UniqueConstraint(
                fields=[
                    "archived_programme",
                    "archived_cost_centre",
                    "archived_natural_account_code",
                ],
                name="archived_financial_row_unique_3",
                condition=Q(archived_analysis1_code__isnull=True)
                & Q(archived_analysis2_code__isnull=True)
                & Q(archived_project_code__isnull=True),
            ),
        ]

    archived_programme = models.ForeignKey(
        ArchivedProgrammeCode, on_delete=models.PROTECT
    )
    archived_cost_centre = models.ForeignKey(
        HistoricCostCentre, on_delete=models.PROTECT
    )
    archived_natural_account_code = models.ForeignKey(
        ArchivedNaturalCode, on_delete=models.PROTECT
    )
    archived_analysis1_code = models.ForeignKey(
        ArchivedAnalysis1, on_delete=models.PROTECT, blank=True, null=True
    )
    archived_analysis2_code = models.ForeignKey(
        ArchivedAnalysis2, on_delete=models.PROTECT, blank=True, null=True
    )
    archived_project_code = models.ForeignKey(
        ArchivedProjectCode, on_delete=models.PROTECT, blank=True, null=True
    )

    forecast_expenditure_type = models.ForeignKey(
        ForecastExpenditureType,
        on_delete=models.PROTECT,
        default=1,
        blank=True,
        null=True,
    )
    def save(self, *args, **kwargs):
        # Override save to calculate the forecast_expenditure_type.
        if self.pk is None:
            # calculate the forecast_expenditure_type
            nac_economic_budget_code = self.archived_natural_account_code.economic_budget_code
            programme_budget_type = self.programme.budget_type_fk

            forecast_type = ForecastExpenditureType.objects.filter(
                programme_budget_type=programme_budget_type,
                nac_economic_budget_code=nac_economic_budget_code,
            )

            self.forecast_expenditure_type = forecast_type.first()

        super(ArchivedFinancialCode, self).save(*args, **kwargs)


class ArchivedForecastData(models.Model):
    financial_code = models.ForeignKey(ArchivedFinancialCode, on_delete=models.PROTECT,)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT,)
    budget = models.BigIntegerField(default=0)
    apr = models.BigIntegerField(default=0)
    may = models.BigIntegerField(default=0)
    jun = models.BigIntegerField(default=0)
    jul = models.BigIntegerField(default=0)
    aug = models.BigIntegerField(default=0)
    sep = models.BigIntegerField(default=0)
    oct = models.BigIntegerField(default=0)
    nov = models.BigIntegerField(default=0)
    dec = models.BigIntegerField(default=0)
    jan = models.BigIntegerField(default=0)
    feb = models.BigIntegerField(default=0)
    mar = models.BigIntegerField(default=0)
    adj1 = models.BigIntegerField(default=0)
    adj2 = models.BigIntegerField(default=0)
    adj3 = models.BigIntegerField(default=0)
    objects = models.Manager()  # The default manager.
    view_data = DisplaySubTotalManager()
