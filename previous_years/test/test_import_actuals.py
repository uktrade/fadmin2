from core.models import FinancialYear

from forecast.import_actuals import (
    save_trial_balance_row,
)

from forecast.models import (
    FinancialPeriod,
)

from previous_years.models import ArchivedActualUploadMonthlyFigure
from previous_years.test.test_utils import (
    PastYearForecastSetup,
)


class ImportPastYearActualTest(PastYearForecastSetup):
    def setUp(self):
        super().setUp()


    def test_import_adj_2(self):
        chart_of_account_line_correct = \
            f'3000-30000-{self.cost_centre_code}-{self.natural_account_code}-{self.programme_code}-00000-00000-0000-0000-0000'

        period_obj = FinancialPeriod.objects.get(
            period_calendar_code=13
            
        )
        year_obj = FinancialYear.objects.get(
            financial_year=self.archived_year
        )
        self.assertEqual(
            ArchivedActualUploadMonthlyFigure.objects.all().count(),
            0,
        )
        save_trial_balance_row(
            chart_of_account_line_correct,
            self.test_amount,
            period_obj,
            year_obj,
            self.check_financial_code,
            2,
            ArchivedActualUploadMonthlyFigure
        )
        # Check that there is a row in the temporary table


        self.assertEqual(
            ArchivedActualUploadMonthlyFigure.objects.all().count(),
            1,
        )
