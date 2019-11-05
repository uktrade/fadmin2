from django.test import RequestFactory, TestCase

from chartofaccountDIT.test.factories import (
    NaturalCodeFactory,
    ProgrammeCodeFactory,
)

from core.models import FinancialYear

from costcentre.test.factories import CostCentreFactory

from forecast.import_actuals import save_row
from forecast.models import (
    FinancialPeriod,
    MonthlyFigure,
)

TEST_COST_CENTRE = 109189
TEST_NATURL_ACCOUNT_CODE = 52191003
TEST_PROGRAMME_CODE = '310940'


class SaveRowTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.cost_centre_code = TEST_COST_CENTRE
        self.natural_account_code = TEST_NATURL_ACCOUNT_CODE
        self.programme_code = TEST_PROGRAMME_CODE

        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=self.cost_centre_code
        )
        self.natural_account = NaturalCodeFactory.create(
            natural_account_code=self.natural_account_code
        )
        self.programme = ProgrammeCodeFactory.create(
            programme_code=self.programme_code
        )
        self.period_obj = FinancialPeriod.objects.get(financial_period_code=2)
        self.year_obj = FinancialYear.objects.get(financial_year=2019)

        self.chart_of_account_line = \
            '3000-30000-{}-{}-{}-00000-00000-0000-0000-0000'.format(
                self.cost_centre_code,
                self.natural_account_code,
                self.programme_code
            )

    def test_save_row(self):
        self.assertEqual(
            MonthlyFigure.objects.filter(cost_centre=self.cost_centre).count(),0)
        save_row(self.chart_of_account_line, 1000, self.period_obj, self.year_obj)
        self.assertEqual(
            MonthlyFigure.objects.filter(cost_centre=self.cost_centre).count(),1)

