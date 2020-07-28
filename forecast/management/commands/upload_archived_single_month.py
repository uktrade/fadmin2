import csv
import logging
from decimal import Decimal

from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.db import connection

from end_of_month.models import EndOfMonthStatus

from core.import_csv import (
    csv_header_to_dict,
    get_fk,
)

from forecast.import_csv import WrongChartOFAccountCodeException
from forecast.models import (
    ActualUploadMonthlyFigure,
    FinancialPeriod,
    FinancialYear,
    ForecastMonthlyFigure,
)
from forecast.utils.import_helpers import CheckFinancialCode


logger = logging.getLogger(__name__)


class WrongArchivePeriodException(Exception):
    pass


def sql_for_single_month_copy(
    financial_period_id, archived_period_id, financial_year_id,
):
    sql_insert = (
        f"INSERT INTO forecast_forecastmonthlyfigure (created, "
        f"updated, amount, starting_amount, financial_code_id, "
        f"financial_period_id, financial_year_id, archived_status_id) "
        f"SELECT now(), now(), amount, amount, financial_code_id, "
        f"financial_period_id, financial_year_id, {archived_period_id} "
        f"FROM forecast_actualuploadmonthlyfigure "
        f"WHERE "
        f"financial_period_id = {financial_period_id} and "
        f"financial_year_id = {financial_year_id} ; "
    )
    return sql_insert


def import_single_archived_period(csvfile, month_to_upload, archive_period, fin_year):

    if month_to_upload <= archive_period:
        raise WrongArchivePeriodException(
            "You are trying to amend Actuals. Only forecast can be amended."
        )

    end_of_month_info = EndOfMonthStatus.objects.get(
        archived_period__financial_period_code=archive_period, archived=True
    )
    if not end_of_month_info:
        raise WrongArchivePeriodException(
            f"There is no archive for period {archive_period} "
        )

    period_obj = FinancialPeriod.objects.get(pk=month_to_upload)

    archive_period_id = end_of_month_info.id
    ActualUploadMonthlyFigure.objects.filter(
        financial_year=fin_year, financial_period=period_obj
    ).delete()

    reader = csv.reader(csvfile)
    col_key = csv_header_to_dict(next(reader))
    line = 1
    fin_obj, msg = get_fk(FinancialYear, fin_year)
    period_obj = FinancialPeriod.objects.get(pk=month_to_upload)

    month_col = col_key[period_obj.period_short_name.lower()]
    check_financial_code = CheckFinancialCode(None)

    csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for row in csv_reader:
        line += 1
        programme_code = row[col_key["programme"]].strip()
        cost_centre = row[col_key["cost centre"]].strip()
        nac = row[col_key["natural account"]].strip()
        analysis1 = row[col_key["analysis"]].strip()
        analysis2 = row[col_key["analysis2"]].strip()
        project_code = row[col_key["project"]].strip()
        check_financial_code.validate(
            cost_centre, nac, programme_code, analysis1, analysis2, project_code, line
        )

        if check_financial_code.error_found:
            raise WrongChartOFAccountCodeException(
                f"Overwriting period, Row {line} error: "
                f"{check_financial_code.display_error}"
            )

        financialcode_obj = check_financial_code.get_financial_code()
        period_amount = Decimal(row[month_col])
        if period_amount:
            month_figure_obj, created = ActualUploadMonthlyFigure.objects.get_or_create(
                financial_year=fin_obj,
                financial_period=period_obj,
                financial_code=financialcode_obj,
            )
            if created:
                month_figure_obj.amount = period_amount * 100
            else:
                month_figure_obj.amount += period_amount * 100
            month_figure_obj.current_amount = month_figure_obj.amount
            month_figure_obj.save()

        if (line % 100) == 0:
            logger.info(line)

    # Now copy the newly uploaded actuals to the monthly figure table
    ForecastMonthlyFigure.objects.filter(
        financial_year=fin_year,
        financial_period=period_obj,
        archived_status_id=archive_period_id,
    ).delete()
    sql_insert = sql_for_single_month_copy(month_to_upload, archive_period_id, fin_year)
    with connection.cursor() as cursor:
        cursor.execute(sql_insert)
    ForecastMonthlyFigure.objects.filter(
        financial_year=fin_year,
        financial_period=period_obj,
        amount=0,
        starting_amount=0,
        archived_status_id=archive_period_id,
    ).delete()
    ActualUploadMonthlyFigure.objects.filter(
        financial_year=fin_year, financial_period=period_obj
    ).delete()

    return True, "Single month import completed successfully."


class Command(BaseCommand):
    help = "Overwrite a specific month in a specific archive"

    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("period_upload", type=int)
        parser.add_argument("archive_period", type=int)
        parser.add_argument("financial_year", type=int)

    def handle(self, *args, **options):
        path = options["path"]
        period = options["period_upload"]
        archive_period = options["archive_period"]
        year = options["financial_year"]

        if period > 15 or period < 1:
            self.stdout.write(self.style.ERROR("Valid Period is between 1 and 15."))
            return

        if archive_period > 15 or archive_period < 1:
            self.stdout.write(
                self.style.ERROR("Valid archive Period is between 1 and 15.")
            )
            return

        # Windows-1252 or CP-1252, used because of a back quote
        csvfile = open(path, newline="", encoding="cp1252")

        try:
            import_single_archived_period(csvfile, period, archive_period, year)
        except (WrongChartOFAccountCodeException, WrongArchivePeriodException) as ex:
            raise CommandError(f"Failure uploading forecast period: {str(ex)}")
            csvfile.close()
            return

        csvfile.close()
        self.stdout.write(
            self.style.SUCCESS(
                f"Updated figures for period {period} "
                f"in archive for period {archive_period}"
            )
        )
