from core.import_csv import (
    IMPORT_CSV_FIELDLIST_KEY,
    IMPORT_CSV_MODEL_KEY,
    IMPORT_CSV_PK_KEY,
    IMPORT_CSV_PK_NAME_KEY,
    import_obj,
)

from costcentre.models import ArchivedCostCentre

from forecast.import_csv import WrongChartOFAccountCodeException

from previous_years.utils import (
    ArchiveYearError,
    validate_year_for_archiving,
)



COST_CENTRE_HISTORICAL_KEY = {
    IMPORT_CSV_MODEL_KEY: ArchivedCostCentre,
    IMPORT_CSV_PK_KEY: "Cost Centre",
    IMPORT_CSV_PK_NAME_KEY: ArchivedCostCentre.chart_of_account_code_name,
    IMPORT_CSV_FIELDLIST_KEY: {
        CostCentre.cost_centre_name.field_name: "Cost Centre Description",
        CostCentre.active.field_name: "Active",
    },
}


def import_archived_cost_centre(csvfile, year):
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(
            f"Failure import Importing archived Cost Centre hierarchy  error: {str(ex)}"
        )
    success, msg = import_obj(csvfile, COST_CENTRE_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(
            f"Importing archived Cost Centre hierarchy  error: " f"{msg}"
        )
    return success, msg

