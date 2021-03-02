from core.models import FinancialYear

from forecast.import_actuals import save_trial_balance_row

from forecast.models import FinancialPeriod

from previous_years.import_actuals import copy_previous_year_actuals_to_monthly_figure
from previous_years.models import (
    ArchivedActualUploadMonthlyFigure,
    ArchivedForecastData,
)
from previous_years.utils import CheckArchivedFinancialCode
from previous_years.test.test_utils import PastYearForecastSetup

from upload_file.models import FileUpload


class ImportPastYearActualTest(PastYearForecastSetup):
    def setUp(self):
        super().setUp()
        dummy_upload = FileUpload(
            s3_document_file="dummy.csv",
            uploading_user=self.test_user,
            document_type=FileUpload.ACTUALS,
        )
        dummy_upload.save()
        self.check_financial_code = CheckArchivedFinancialCode(
            self.archived_year, dummy_upload
        )
        self.year_obj = FinancialYear.objects.get(financial_year=self.archived_year)
        self.year_obj.current = False
        self.year_obj.save()
        self.chart_of_account_line_correct = (
            f"3000-30000-"
            f"{self.cost_centre_code}-"
            f"{self.natural_account_code}-"
            f"{self.programme_code}-"
            f"{self.analisys1}-"
            f"{self.analisys2}-"
            f"{self.project_code}-"
            f"0000-"
            f"0000-0000"
        )

    def test_import_adj_2(self):
        period_obj = FinancialPeriod.objects.get(period_calendar_code=13)
        period_name = period_obj.period_short_name.lower()
        self.assertEqual(
            ArchivedActualUploadMonthlyFigure.objects.all().count(), 0,
        )
        self.assertEqual(
            ArchivedForecastData.objects.all().count(), 1,
        )
        data_obj = ArchivedForecastData.objects.all().first()
        new_value_in_pence = 23456700
        self.assertNotEqual(
            getattr(data_obj, period_name), new_value_in_pence,
        )

        save_trial_balance_row(
            self.chart_of_account_line_correct,
            new_value_in_pence/100,
            period_obj,
            self.year_obj,
            self.check_financial_code,
            2,
            ArchivedActualUploadMonthlyFigure,
        )
        # Check that there is a row in the temporary table
        self.assertEqual(
            ArchivedActualUploadMonthlyFigure.objects.all().count(), 1,
        )
        copy_previous_year_actuals_to_monthly_figure(period_obj, self.archived_year)
        self.assertEqual(
            ArchivedForecastData.objects.all().count(), 1,
        )
        data_obj = ArchivedForecastData.objects.all().first()
        # Check that the field has been updated with the new value
        self.assertEqual(
            getattr(data_obj, period_name), new_value_in_pence,
        )
