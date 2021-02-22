import logging

from django.db import connection

from core.import_csv import get_fk, get_fk_from_field
from core.models import FinancialYear

from forecast.models import (
    ActualUploadMonthlyFigure,
    FinancialPeriod,
    ForecastMonthlyFigure,
)
from forecast.utils.import_helpers import (
    CheckFinancialCode,
    UploadFileFormatError,
    sql_for_data_copy,
    validate_excel_file,
)

from previous_years.utils import CheckArchivedFinancialCode

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
)

logger = logging.getLogger(__name__)

def copy_previous_year_actuals_to_monthly_figure(period_obj, year):
    # # Now copy the newly uploaded actuals to the previous year figure table
    # hack alert: the name of the fields in the model are identical to the short name
    # of the period, but in lowercase
    period_name = period_obj.period_short_name.lower()
    sql_update = "UPDATE "
    pass
    # ForecastMonthlyFigure.objects.filter(
    #     financial_year=year, financial_period=period_obj, archived_status__isnull=True,
    # ).update(amount=0, starting_amount=0)
    # sql_update, sql_insert = sql_for_data_copy(FileUpload.ACTUALS, period_obj.pk, year)
    # with connection.cursor() as cursor:
    #     cursor.execute(sql_insert)
    #     cursor.execute(sql_update)
    # ForecastMonthlyFigure.objects.filter(
    #     financial_year=year,
    #     financial_period=period_obj,
    #     amount=0,
    #     starting_amount=0,
    #     archived_status__isnull=True,
    # ).delete()


