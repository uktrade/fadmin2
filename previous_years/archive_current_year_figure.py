import datetime
import logging

from core.models import FinancialYear

from forecast.utils.import_helpers import (
    UploadFileDataError,
    UploadFileFormatError,
)
from forecast.utils.query_fields import ForecastQueryFields

from previous_years.import_previous_year import (
    copy_previous_year_figure_from_temp_table,
)
from previous_years.models import (
    ArchivedForecastData,
    ArchivedForecastDataUpload,
)
from previous_years.utils import (
    ArchiveYearError,
    CheckArchivedFinancialCode,
    validate_year_for_archiving_actuals,
)

from upload_file.models import FileUpload
from upload_file.utils import (
    set_file_upload_fatal_error,
    set_file_upload_feedback,
)
logger = logging.getLogger(__name__)



def archive_to_temp_previous_year_figures(
    row_to_archive, financial_year_obj, financialcode_obj
):
        (
            previous_year_obj,
            created,
        ) = ArchivedForecastDataUpload.objects.get_or_create(
            financial_year=financial_year_obj, financial_code=financialcode_obj,
        )
        # to avoid problems with precision,
        # we store the figures in pence
        if created:
            previous_year_obj.budget = row_to_archive["budget"]
            previous_year_obj.apr = row_to_archive["apr"]
            previous_year_obj.may = row_to_archive["may"]
            previous_year_obj.jun = row_to_archive["jun"]
            previous_year_obj.jul = row_to_archive["jul"]
            previous_year_obj.aug = row_to_archive["aug"]
            previous_year_obj.sep = row_to_archive["sep"]
            previous_year_obj.oct = row_to_archive["oct"]
            previous_year_obj.nov = row_to_archive["nov"]
            previous_year_obj.dec = row_to_archive["dec"]
            previous_year_obj.jan = row_to_archive["jan"]
            previous_year_obj.feb = row_to_archive["feb"]
            previous_year_obj.mar = row_to_archive["mar"]
            previous_year_obj.adj1 = row_to_archive["adj01"]
            previous_year_obj.adj2 = row_to_archive["adj02"]
            previous_year_obj.adj3 = row_to_archive["adj03"]
        else:
            previous_year_obj.budget += row_to_archive["budget"]
            previous_year_obj.apr += row_to_archive["apr"]
            previous_year_obj.may += row_to_archive["may"]
            previous_year_obj.jun += row_to_archive["jun"]
            previous_year_obj.jul += row_to_archive["jul"]
            previous_year_obj.aug += row_to_archive["aug"]
            previous_year_obj.sep += row_to_archive["sep"]
            previous_year_obj.oct += row_to_archive["oct"]
            previous_year_obj.nov += row_to_archive["nov"]
            previous_year_obj.dec += row_to_archive["dec"]
            previous_year_obj.jan += row_to_archive["jan"]
            previous_year_obj.feb += row_to_archive["feb"]
            previous_year_obj.mar += row_to_archive["mar"]
            previous_year_obj.adj1 += row_to_archive["adj01"]
            previous_year_obj.adj2 += row_to_archive["adj02"]
            previous_year_obj.adj3 += row_to_archive["adj03"]
        previous_year_obj.save()


def archive_current_year():

    fields = ForecastQueryFields(0)
    financial_year = fields.selected_year
    datamodel = fields.datamodel

    data_to_archive_list = datamodel.view_data.raw_data_annotated(
        fields.ARCHIVE_FORECAST_COLUMNS, {}, year=financial_year
    )
    financial_year_obj = FinancialYear.objects.get(pk=financial_year)

    # Clear the table used to upload the previous_years.
    # The previous_years are uploaded to to a temporary storage, and copied
    # when the upload is completed successfully.
    # This means that we always have a full upload.
    ArchivedForecastDataUpload.objects.filter(financial_year=financial_year,).delete()
    rows_to_process = data_to_archive_list.count()

    check_financial_code = CheckArchivedFinancialCode(financial_year)
    row_number = 0
    for row_to_archive in data_to_archive_list:
        if not row_number % 100:
             logger.info(f"Processing row {row_number} of {rows_to_process}.")

        cost_centre = row_to_archive["cost_centre"]
        if not cost_centre:
            # protection against empty rows
            break
        nac = row_to_archive["nac"]
        programme_code = row_to_archive["pogramme_code"]
        analysis1 = row_to_archive["analysis1"]
        analysis2 = row_to_archive["analysis2"]
        project_code = row_to_archive["project_code"]
        check_financial_code.validate(
            cost_centre,
            nac,
            programme_code,
            analysis1,
            analysis2,
            project_code,
            row_number,
        )
        if not check_financial_code.error_found:
            financialcode_obj = check_financial_code.get_financial_code()
            try:
                archive_to_temp_previous_year_figures(
                    row_to_archive,
                    financial_year_obj,
                    financialcode_obj,
                )
            except (UploadFileFormatError, ArchiveYearError) as ex:
                set_file_upload_fatal_error(
                    file_upload, str(ex), str(ex),
                )
                raise ex

    final_status = FileUpload.PROCESSED
    if check_financial_code.error_found:
        final_status = FileUpload.PROCESSEDWITHERROR
    else:
        # No errors, so we can copy the figures
        # from the temporary table to the previous_years
        copy_previous_year_figure_from_temp_table(financial_year)
        if check_financial_code.warning_found:
            final_status = FileUpload.PROCESSEDWITHWARNING

    set_file_upload_feedback(
        file_upload, f"Processed {rows_to_process} rows.", final_status
    )

    if check_financial_code.error_found:
        raise UploadFileDataError(
            "No data archived. Check the log in the file upload record."
        )
