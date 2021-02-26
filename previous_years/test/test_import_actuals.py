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

# ADD MIGRATION FOR FIXING ADJ

class ImportPastYearActualTest(PastYearForecastSetup):
    def setUp(self):
        super().setUp()


    def test_import_adj_2(self):
        chart_of_account_line_correct = \
            f'3000-30000-{self.cost_centre_code}-{self.valid_natural_account_code}-{self.programme_code}-00000-00000-0000-0000-0000'

        period_obj = FinancialPeriod.objects.get(
            period_calendar_code=13
        )
        year_obj = FinancialYear.objects.get(
            financial_year=self.archived_year
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
