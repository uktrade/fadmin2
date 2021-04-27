# from django.db import connection

from core.import_csv import xslx_header_to_dict

from split_project.models import UploadProjectSplitCoefficient
from forecast.models import FinancialPeriod


from forecast.utils.import_helpers import (
    CheckFinancialCode,
    UploadFileDataError,
    UploadFileFormatError,
    check_header,
    validate_excel_file,
)

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
)

EXPECTED_PERCENTAGE_HEADERS = [
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
    "adj1",
    "adj2",
    "adj3",
]


def copy_uploaded_percentage(month_dict):
    # for period_obj in month_dict.values():
    #     # Now copy the newly uploaded budgets to the monthly figure table
    #     BudgetMonthlyFigure.objects.filter(
    #         financial_year=year,
    #         financial_period=period_obj,
    #         archived_status__isnull=True,
    #     ).update(amount=0, starting_amount=0)
    #     sql_update, sql_insert = sql_for_data_copy(
    #         FileUpload.BUDGET, period_obj.pk, year
    #     )
    #     with connection.cursor() as cursor:
    #         cursor.execute(sql_insert)
    #         cursor.execute(sql_update)
    #     BudgetMonthlyFigure.objects.filter(
    #         financial_year=year,
    #         financial_period=period_obj,
    #         amount=0,
    #         starting_amount=0,
    #         archived_status__isnull=True,
    #     ).delete()
    UploadProjectSplitCoefficient.objects.delete()


def upload_project_percentage_row(
    percentage_row, financialcode_obj_to, financialcode_obj_from, month_dict
):
    for month_idx, period_obj in month_dict.items():
        period_percentage = percentage_row[month_idx].value
        if period_percentage is None:
            period_percentage = 0
        # We import from Excel, and the user may have entered spaces in an empty cell.
        if type(period_percentage) == str:
            period_percentage = period_percentage.strip()
        if period_percentage == "-":
            # we accept the '-' as it is a recognised value in Finance for 0
            period_percentage = 0
        try:
            period_percentage = period_percentage * 100.00
        except ValueError:
            raise UploadFileDataError(
                f"Non-numeric value in {percentage_row[month_idx].coordinate}:{period_percentage}"  # noqa
            )
        if period_percentage:
            (
                percentage_obj,
                created,
            ) = UploadProjectSplitCoefficient.objects.get_or_create(
                financial_period=period_obj,
                financial_code_from=financialcode_obj_from,
                financial_code_to=financialcode_obj_to,
            )
            if created:
                percentage_obj.amount = period_percentage
                percentage_obj.save()
            else:
                raise UploadFileDataError("Duplicate row.")


def create_month_dict(header_dict):
    month_dict = {}
    for month in FinancialPeriod.objects.all():
        month_name = month.period_short_name.lower()
        if month_name in header_dict:
            month_dict[header_dict[month_name]] = month
    return month_dict


def upload_project_percentage(worksheet, header_dict, file_upload):
    # Clear the table used to upload the percentages.
    # The percentages are uploaded to to a temporary storage, and copied
    # when the upload is completed successfully.
    # This means that we always have a full upload.
    UploadProjectSplitCoefficient.objects.delete()
    rows_to_process = worksheet.max_row + 1
    month_dict = create_month_dict(header_dict)
    check_financial_code = CheckFinancialCode(file_upload)
    cc_index = header_dict["cost centre"]
    nac_index = header_dict["natural account"]
    prog_index = header_dict["programme"]
    a1_index = header_dict["analysis"]
    a2_index = header_dict["analysis2"]
    proj_index = header_dict["project"]
    row_number = 0
    # There is a terrible performance hit accessing the individual cells:
    # The cell is found starting from cell A0, and continuing until the
    # required cell is found
    # The rows in worksheet.rows are accessed sequentially, so there is no
    # performance problem.
    # A typical files took over 2 hours to read using the cell access method
    # and 10 minutes with the row access.
    for percentage_row in worksheet.rows:
        row_number += 1
        if row_number == 1:
            # There is no way to start reading rows from a specific place.
            # Ignore first row, the headers have been processed already
            continue
        if not row_number % 100:
            # Display the number of rows processed every 100 rows
            set_file_upload_feedback(
                file_upload, f"Processing row {row_number} of {rows_to_process}."
            )
        cost_centre = percentage_row[cc_index].value
        if not cost_centre:
            # protection against empty rows
            break
        check_financial_code.validate(
            cost_centre,
            percentage_row[nac_index].value,
            percentage_row[prog_index].value,
            percentage_row[a1_index].value,
            percentage_row[a2_index].value,
            percentage_row[proj_index].value,
            row_number,
        )
        if not check_financial_code.error_found:
            try:
                upload_project_percentage_row(
                    percentage_row,
                    check_financial_code.get_financial_code(),
                    check_financial_code.get_financial_code_no_project(),
                    month_dict,
                )
            except UploadFileDataError as ex:
                check_financial_code.record_error(row_number, str(ex))

    final_status = FileUpload.PROCESSED
    if check_financial_code.error_found:
        final_status = FileUpload.PROCESSEDWITHERROR
    else:
        # No errors, so we can copy the figures
        # from the temporary table to the percentages
        copy_uploaded_percentage()
        if check_financial_code.warning_found:
            final_status = FileUpload.PROCESSEDWITHWARNING

    set_file_upload_feedback(
        file_upload, f"Processed {rows_to_process} rows.", final_status
    )
    return not check_financial_code.error_found


def upload_project_percentage_from_file(file_upload):
    try:
        workbook, worksheet = validate_excel_file(file_upload, "Project Percentages")
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        raise ex
    header_dict = xslx_header_to_dict(worksheet[1])
    try:
        check_header(header_dict, EXPECTED_PERCENTAGE_HEADERS)
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    try:
        upload_project_percentage(worksheet, header_dict, file_upload)
    except (UploadFileDataError) as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        workbook.close
        raise ex
    workbook.close
