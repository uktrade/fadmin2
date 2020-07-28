import csv
import logging
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import connection

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


def sql_for_single_month_copy(
    financial_period_id, archived_period_id, financial_year_id,
):
    if archived_period_id != 0:
        archived_filter = "= {archived_period_id}"
        archived_value = f"{archived_period_id}"
    else:
        archived_filter = "IS NULL"
        archived_value = "NULL"

    sql_update = (
        f"UPDATE forecast_forecastmonthlyfigure t "
        f"SET  updated=now(), amount=u.amount, starting_amount=u.starting_amount, "
        f"archived_status_id = {archived_value}"
        f"FROM forecast_budgetuploadmonthlyfigure u "
        f"WHERE  "
        f"t.financial_code_id = u.financial_code_id and "
        f"t.financial_period_id = u.financial_period_id and "
        f"t.financial_year_id = u.financial_year_id and "
        f"t.financial_period_id = {financial_period_id} and "
        f"t.archived_status_id {archived_filter} and "
        f"t.financial_year_id = {financial_year_id};"
    )

    sql_insert = (
        f"INSERT INTO forecast_forecastmonthlyfigure (created, "
        f"updated, amount, starting_amount, financial_code_id, "
        f"financial_period_id, financial_year_id, archived_status_id) "
        f"SELECT now(), now(), amount, amount, financial_code_id, "
        f"financial_period_id, financial_year_id, {archived_value} "
        f"FROM forecast_actualuploadmonthlyfigure "
        f"WHERE "
        f"financial_period_id = {financial_period_id} and "
        f"financial_year_id = {financial_year_id}  and "
        f" financial_code_id "
        f"not in (select financial_code_id "
        f"from forecast_forecastmonthlyfigure where "
        f"financial_period_id = {financial_period_id} and "
        f"archived_status_id {archived_filter}  and "
        f"financial_year_id = {financial_year_id});"
    )

    return sql_update, sql_insert


def import_single_archived_period(csvfile, month_to_upload, archive_period, fin_year):
    period_obj = FinancialPeriod.objects.get(pk=month_to_upload)
    ActualUploadMonthlyFigure.objects.filter(
        financial_year=fin_year, financial_period=period_obj
    ).delete()

    reader = csv.reader(csvfile)
    col_key = csv_header_to_dict(next(reader))
    line = 1
    fin_obj, msg = get_fk(FinancialYear, fin_year)
    period_obj = FinancialPeriod.objects.get(pk=month_to_upload)
    month_col = col_key[period_obj.period_short_name.lower]
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
        archived_status_id=archive_period,
    ).update(amount=0, starting_amount=0)
    sql_update, sql_insert = sql_for_single_month_copy(
        month_to_upload, archive_period, fin_year
    )
    with connection.cursor() as cursor:
        cursor.execute(sql_insert)
        cursor.execute(sql_update)
    ForecastMonthlyFigure.objects.filter(
        financial_year=fin_year,
        financial_period=period_obj,
        amount=0,
        starting_amount=0,
        archived_status_id=archive_period,
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

        import_single_archived_period(path, period, archive_period, year)
        self.stdout.write(
            self.style.SUCCESS("Actual for period {} added".format(period))
        )
