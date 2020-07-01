from django.db import connection

from core.import_csv import xslx_header_to_dict
from core.models import FinancialYear

from forecast.models import (
    BudgetMonthlyFigure,
    BudgetUploadMonthlyFigure,
)
from forecast.utils.import_helpers import (
    CheckFinancialCode,
    UploadFileDataError,
    UploadFileFormatError,
    get_forecast_month_dict,
    sql_for_data_copy,
    validate_excel_file,
)

from core.import_csv import (
    get_fk,
    get_fk_from_field,
    get_pk_verbose_name,
)

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
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
    for period_obj in month_dict.values():
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
    BudgetUploadMonthlyFigure.objects.filter(financial_year=year).delete()

# This is where you un-indented it
CODE_OK = 1
CODE_ERROR = 2
CODE_WARNING = 3
IGNORE = 4

obj_index = 0
status_index = 1
message_index = 2

VALID_ECONOMIC_CODE_LIST = ["RESOURCE", "CAPITAL"]

# class CheckUploadBudgetFigures:
display_error = ""
display_warning = ""
financial_code_obj = None
error_found = False
warning_found = False
ignore_row = False
# Dictionary of tuples
# Each tuple contains : (obj, status, error_code, message)
# The objects of codes already used are kept in the dictionary,
# to reduce the number of database accesses
nac_dict = {}
cc_dict = {}
prog_dict = {}
analysis1_dict = {}
analysis2_dict = {}
project_dict = {}

error_row = 0

def get_info_tuple(model, pk):
    obj, msg = get_fk(model, pk)
    if not obj:
        status = CODE_ERROR
    else:
        if not obj.active:
            if upload_type == FileUpload.BUDGET:
                status = CODE_ERROR
                msg = (
                    f'{get_pk_verbose_name(model)} "{pk}" '
                    f"is not in the approved list. \n"
                )
                obj = None
            else:
                obj.active
                obj.save
                status = CODE_WARNING
                msg = (
                    f'{get_pk_verbose_name(model)} "{pk}" '
                    f"added to the approved list. \n"
                )
        else:
            status = CODE_OK
            msg = ""
    info_tuple = (obj, status, msg)
    return info_tuple

def validate_info_tuple(info_tuple):
    status = info_tuple[status_index]
    msg = info_tuple[message_index]
    obj = info_tuple[obj_index]

    if status == CODE_ERROR:
        error_found = True
        display_error = display_error + msg
    else:
        if status == CODE_WARNING:
            warning_found = True
            display_warning = display_warning + msg
    return obj

def get_obj_code(code_dict, code, model_name):
    # protection in case the code was read from an empty cell
    if code is None:
        code = 0
    info_tuple = code_dict.get(code, None)
    if not info_tuple:
        info_tuple = get_info_tuple(model_name, code)
        code_dict[code] = info_tuple
    return validate_info_tuple(info_tuple)

def upload_budget_figures(budget_row, year_obj, financialcode_obj, month_dict):
    for month_idx, period_obj in month_dict.items():
        period_budget = budget_row[month_idx].value
        # print(period_budget)
        for i in range(period_budget):
            # print(period_budget)
            if i == '-':
                i == 0
            elif type(i) != int:
                info_tuple = get_info_tuple(period_budget)
                if info_tuple[status_index] == CODE_OK:
                    obj = info_tuple[obj_index]
                    if not obj.used_for_budget:
                        status = CODE_WARNING
                        msg = f'Budget figure "{period_budget}" is not a number.\n'
                        info_tuple = (obj, status, msg)

                return validate_info_tuple(info_tuple)

    if period_budget:
        (budget_obj, created,) = BudgetUploadMonthlyFigure.objects.get_or_create(
            financial_year=year_obj,
            financial_code=financialcode_obj,
            financial_period=period_obj,
        )
        # to avoid problems with precision,
        # we store the figures in pence
        if created:
            budget_obj.amount = period_budget * 100
        else:
            budget_obj.amount += period_budget * 100
        budget_obj.save()

def upload_budget(worksheet, year, header_dict, file_upload):
    year_obj, created = FinancialYear.objects.get_or_create(financial_year=year)
    if created:
        year_obj.financial_year_display = f"{year}/{year - 1999}"
        year_obj.save()

    forecast_months = get_forecast_month_dict()
    month_dict = {header_dict[k]: v for (k, v) in forecast_months.items()}
    # Clear the table used to upload the budgets.
    # The budgets are uploaded to to a temporary storage, and copied
    # when the upload is completed successfully.
    # This means that we always have a full upload.
    BudgetUploadMonthlyFigure.objects.filter(financial_year=year,).delete()
    rows_to_process = worksheet.max_row + 1

    check_financial_code = CheckFinancialCode(file_upload)
    cc_index = header_dict["cost centre"]
    nac_index = header_dict["natural account"]
    prog_index = header_dict["programme"]
    a1_index = header_dict["analysis"]
    a2_index = header_dict["analysis2"]
    proj_index = header_dict["project"]
    row = 0
    # There is a terrible performance hit accessing the individual cells:
    # The cell is found starting from cell A0, and continuing until the
    # required cell is found
    # The rows in worksheet.rows are accessed sequentially, so there is no
    # performance problem.
    # A typical files took over 2 hours to read using the cell access method
    # and 10 minutes with the row access.
    for budget_row in worksheet.rows:
        row += 1
        if row == 1:
            # There is no way to start reading rows from a specific place.
            # Ignore first row, the headers have been processed already
            continue
        if not row % 100:
            # Display the number of rows processed every 100 rows
            set_file_upload_feedback(
                file_upload, f"Processing row {row} of {rows_to_process}."
            )
        cost_centre = budget_row[cc_index].value
        if not cost_centre:
            # protection against empty rows
            break
        nac = budget_row[nac_index].value
        programme_code = budget_row[prog_index].value
        analysis1 = budget_row[a1_index].value
        analysis2 = budget_row[a2_index].value
        project_code = budget_row[proj_index].value
        check_financial_code.validate(
            cost_centre, nac, programme_code, analysis1, analysis2, project_code, row
        )

        if not check_financial_code.error_found:
            financialcode_obj = check_financial_code.get_financial_code()
            upload_budget_figures(budget_row, year_obj, financialcode_obj, month_dict)

    final_status = FileUpload.PROCESSED
    if check_financial_code.error_found:
        final_status = FileUpload.PROCESSEDWITHERROR
    else:
        # No errors, so we can copy the figures from the temporary table to the budgets
        copy_uploaded_budget(year, month_dict)
        if check_financial_code.warning_found:
            final_status = FileUpload.PROCESSEDWITHWARNING

    set_file_upload_feedback(
        file_upload, f"Processed {rows_to_process} rows.", final_status
    )

    return not check_financial_code.error_found

def upload_budget_from_file(file_upload, year):
    try:
        workbook, worksheet = validate_excel_file(file_upload, "Budgets")
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        raise ex
    header_dict = xslx_header_to_dict(worksheet[1])
    try:
        check_budget_header(header_dict, EXPECTED_BUDGET_HEADERS)
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    try:
        upload_budget(worksheet, year, header_dict, file_upload)
    except (UploadFileDataError) as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    workbook.close