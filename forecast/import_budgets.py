from django.db import connection


from core.import_csv import get_fk, xslx_header_to_dict
from core.models import FinancialYear

from forecast.import_utils import (
    CheckFinancialCode,
    UploadFileDataError,
    UploadFileFormatError,
    get_forecast_month_dict,
    sql_for_data_copy,
    validate_excel_file,
)
from forecast.models import (
    BudgetMonthlyFigure,
    BudgetUploadMonthlyFigure,
)

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_error,
    set_file_upload_feedback,
    set_incremental_file_upload_error,
)

EXPECTED_BUDGET_HEADERS = [
    "cost centre",
    "natural account",
    "programme",
    "analysis",
    "analysis2",
    "project",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
    "jan",
    "feb",
    "mar",
]


def check_budget_header(header_dict, correct_header):
    error_msg = ""
    correct = True
    for elem in correct_header:
        if elem not in header_dict:
            correct = False
            error_msg += f"'{elem}' not found. "
    if not correct:
        raise UploadFileFormatError(f"Error in the header: {error_msg}")


def copy_uploaded_budget(year, month_dict):
    for m, period_obj in month_dict.items():
        # Now copy the newly uploaded budgets to the monthly figure table
        BudgetMonthlyFigure.objects.filter(
            financial_year=year, financial_period=period_obj,
        ).update(amount=0, starting_amount=0)
        sql_update, sql_insert = sql_for_data_copy(
            FileUpload.BUDGET, period_obj.pk, year
        )
        with connection.cursor() as cursor:
            cursor.execute(sql_insert)
            cursor.execute(sql_update)
        BudgetMonthlyFigure.objects.filter(
            financial_year=year,
            financial_period=period_obj,
            amount=0,
            starting_amount=0,
        ).delete()
        BudgetUploadMonthlyFigure.objects.filter(
            financial_year=year, financial_period=period_obj
        ).delete()


def upload_budget(worksheet, year, header_dict, file_upload):
    year_obj, created = FinancialYear.objects.get_or_create(financial_year=year)
    if created:
        year_obj.financial_year_display = f"{year}/{year - 1999}"
        year_obj.save()

    month_dict = get_forecast_month_dict()
    # Clear the table used to upload the budgets.
    # The budgets are uploaded to to a temporary storage, and copied
    # when the upload is completed successfully.
    # This means that we always have a full upload.
    BudgetUploadMonthlyFigure.objects.filter(financial_year=year,).delete()
    rows_to_process = worksheet.max_row + 1

    error_found = False
    warning_message = ""

    for row in range(2, rows_to_process):
        cost_centre = worksheet[f"{header_dict['cost centre']}{row}"].value
        nac = worksheet[f"{header_dict['natural account']}{row}"].value
        programme_code = worksheet[f"{header_dict['programme']}{row}"].value
        analysis1 = worksheet[f"{header_dict['analysis']}{row}"].value
        analysis2 = worksheet[f"{header_dict['analysis2']}{row}"].value
        project_code = worksheet[f"{header_dict['project']}{row}"].value
        check_financial_code = CheckFinancialCode(
            cost_centre, nac, programme_code, analysis1, analysis2, project_code
        )

        if check_financial_code.error_found:
            error_found = True
            set_incremental_file_upload_error(
                file_upload,
                f"Row {row}: {check_financial_code.display_error} not valid.",
                "Upload aborted: Data error.",
            )

        if not error_found:
            if not row % 100:
                set_file_upload_feedback(
                    file_upload, f"Processing row {row} of {rows_to_process}."
                )
            financialcode_obj = check_financial_code.get_financial_code()
            for month, period_obj in month_dict.items():
                period_budget = worksheet[f"{header_dict[month.lower()]}{row}"].value
                if period_budget:
                    (
                        budget_obj,
                        created,
                    ) = BudgetUploadMonthlyFigure.objects.get_or_create(
                        financial_year=year_obj,
                        financial_code=financialcode_obj,
                        financial_period=period_obj,
                    )

                    if created:
                        # to avoid problems with precision,
                        # we store the figures in pence
                        budget_obj.amount = period_budget * 100
                    else:
                        budget_obj.amount += period_budget * 100
                    budget_obj.save()

    if not error_found:
        copy_uploaded_budget(year, month_dict)


def upload_budget_from_file(file_upload, year):
    try:
        workbook, worksheet = validate_excel_file(file_upload, "Budgets")
    except UploadFileFormatError as ex:
        set_file_upload_error(
            file_upload, str(ex), str(ex),
        )
        raise ex
    header_dict = xslx_header_to_dict(worksheet[1])
    try:
        check_budget_header(header_dict, EXPECTED_BUDGET_HEADERS)
    except UploadFileFormatError as ex:
        set_file_upload_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    try:
        upload_budget(worksheet, year, header_dict, file_upload)
    except (UploadFileDataError) as ex:
        set_file_upload_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    workbook.close
    return True
