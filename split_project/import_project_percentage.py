from django.db import connection

from core.import_csv import xslx_header_to_dict

from forecast.models import (
    FinancialPeriod,
    ForecastMonthlyFigure,
)

from split_project.models import (
    ProjectSplitCoefficient,
    UploadProjectSplitCoefficient,
)
from split_project.split_figure import handle_split_project

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

WORKSHEET_PROJECT_TITLE = "Project Percentages"
COST_CENTRE_CODE = "cost centre code"
NAC_CODE = "natural account code"
PROGRAMME_CODE = "programme code"
PROJECT_CODE = "project code"
ANALYSIS1_CODE = "contract code"
ANALYSIS2_CODE = "market code"
EXPECTED_PERCENTAGE_HEADERS = [
    COST_CENTRE_CODE,
    NAC_CODE,
    PROGRAMME_CODE,
    ANALYSIS1_CODE,
    ANALYSIS2_CODE,
    PROJECT_CODE,
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
    for period_obj in month_dict.values():
        # Now copy the newly uploaded budgets to the monthly figure table
        ProjectSplitCoefficient.objects.filter(
            financial_period=period_obj,
        ).delete()
        sql_insert = f"INSERT INTO public.split_project_projectsplitcoefficient" \
                     f"(created, updated, split_coefficient, financial_code_from_id, " \
                     f"financial_code_to_id, financial_period_id)	" \
                     f"SELECT now(), now(), split_coefficient, financial_code_from_id, " \
                     f"financial_code_to_id, financial_period_id " \
                     f"FROM public.split_project_uploadprojectsplitcoefficient " \
                     f"WHERE financial_period_id = {period_obj.financial_period_code};"

        with connection.cursor() as cursor:
            cursor.execute(sql_insert)
        UploadProjectSplitCoefficient.objects.filter(
            financial_period=period_obj,
        ).delete()


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
            period_percentage = int(period_percentage * 10000)
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
                percentage_obj.split_coefficient = period_percentage
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
    # But we ignored previous periods
    UploadProjectSplitCoefficient.objects.all().delete()
    rows_to_process = worksheet.max_row + 1
    month_dict = create_month_dict(header_dict)
    check_financial_code = CheckFinancialCode(file_upload)
    cc_index = header_dict[COST_CENTRE_CODE]
    nac_index = header_dict[NAC_CODE]
    prog_index = header_dict[PROGRAMME_CODE]
    a1_index = header_dict[ANALYSIS1_CODE]
    a2_index = header_dict[ANALYSIS2_CODE]
    proj_index = header_dict[PROJECT_CODE]
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
    # use the project split for the last actuals if needed
    # handle_split_project(
    #     period_obj.financial_period_code,
    #     ForecastMonthlyFigure
    # )

    return not check_financial_code.error_found


def upload_project_percentage_from_file(file_upload):
    try:
        workbook, worksheet = validate_excel_file(file_upload, WORKSHEET_PROJECT_TITLE)
    except UploadFileFormatError as ex:
        set_file_upload_fatal_error(
            file_upload, str(ex), str(ex),
        )
        raise ex
    header_dict = xslx_header_to_dict(worksheet[1])
    try:
        # TODO change it to upload just one month or more
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
