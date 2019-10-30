from forecast.models import (
    Budget,
    FinancialPeriod,
    MonthlyFigure,

)

from core.models import FinancialYear

from costcentre.test.factories import CostCentreFactory

from chartofaccountDIT.test.factories import (
    ProgrammeCodeFactory,
    NaturalCodeFactory,
)

import factory



class BudgetFactory(factory.DjangoModelFactory):
    """
    Define Budget Factory
    """

    class Meta:
        model = Budget


class MonthlyFigureFactory(factory.DjangoModelFactory):
    """
    Define MonthlyFigure Factory
    """
    programme = factory.SubFactory(ProgrammeCodeFactory)
    cost_centre = factory.SubFactory(CostCentreFactory)
    natural_account_code = factory.SubFactory(NaturalCodeFactory)
    financial_year = factory.Iterator(FinancialYear.objects.all())
    financial_period = factory.Iterator(FinancialPeriod.objects.all())
    amount = 123456
    class Meta:
        model = MonthlyFigure


