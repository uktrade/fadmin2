from django.db import models

from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
    BudgetType,
)

from core.metamodels import (
    ArchivedModel,
    BaseModel,
)
from core.models import FinancialYear

from costcentre.models import HistoricCostCentre

from forecast.models import (
    FinancialCodeAbstract,
    ForecastExpenditureType,
    ForecastingDataViewAbstract,
)


class ArchivedFinancialCode(ArchivedModel, FinancialCodeAbstract):
    """Contains the members of Chart of Account needed to create a unique key"""
    programme = models.ForeignKey(
        ArchivedProgrammeCode, on_delete=models.PROTECT
    )
    cost_centre = models.ForeignKey(
        HistoricCostCentre, on_delete=models.PROTECT
    )
    natural_account_code = models.ForeignKey(
        ArchivedNaturalCode, on_delete=models.PROTECT
    )
    analysis1_code = models.ForeignKey(
        ArchivedAnalysis1, on_delete=models.PROTECT, blank=True, null=True
    )
    analysis2_code = models.ForeignKey(
        ArchivedAnalysis2, on_delete=models.PROTECT, blank=True, null=True
    )
    project_code = models.ForeignKey(
        ArchivedProjectCode, on_delete=models.PROTECT, blank=True, null=True
    )

    forecast_expenditure_type = models.ForeignKey(
        ForecastExpenditureType,
        on_delete=models.PROTECT,
        default=1,
        blank=True,
        null=True,
    )


class ArchivedForecastDataAbstract(ForecastingDataViewAbstract, BaseModel):
    financial_code = models.ForeignKey(ArchivedFinancialCode, on_delete=models.PROTECT,)
    class Meta:
        abstract = True


class ArchivedForecastDataUpload(ArchivedForecastDataAbstract):
    pass


class ArchivedForecastData(ArchivedForecastDataAbstract):
    pass
