from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
)

from core.import_csv import (
    IMPORT_CSV_FIELDLIST_KEY,
    IMPORT_CSV_MODEL_KEY,
    IMPORT_CSV_PK_KEY,
    IMPORT_CSV_PK_NAME_KEY,
    import_obj,
)

from forecast.import_csv import WrongChartOFAccountCodeException

from previous_years.utils import (
    ArchiveYearError,
    validate_year_for_archiving,
)

ANALYSIS1_HISTORICAL_KEY = {
    IMPORT_CSV_MODEL_KEY: ArchivedAnalysis1,
    IMPORT_CSV_PK_KEY: "Analysis 1 Code",
    IMPORT_CSV_PK_NAME_KEY: "analysis1_code",
    IMPORT_CSV_FIELDLIST_KEY: {
        "analysis1_description": "Contract Name",
        "supplier": "Supplier",
        "pc_reference": "PC Reference",
    },
}


ANALYSIS2_HISTORICAL_KEY = {
    IMPORT_CSV_MODEL_KEY: ArchivedAnalysis2,
    IMPORT_CSV_PK_KEY: "Market Code",
    IMPORT_CSV_PK_NAME_KEY: "analysis2_code",
    IMPORT_CSV_FIELDLIST_KEY: {
        "analysis2_description": "Market Description",
    },
}


def import_archived_analysis1(csvfile, year):
    try:
        validate_year_for_archiving(year)
    except ArchiveYearError as ex:
        raise ArchiveYearError(
            f"Failure import Importing archived Analysis1 (Contract) error: {str(ex)}"
        )

    success, msg = import_obj(csvfile, ANALYSIS1_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(
            f"Importing archived Analysis1 (Contract) error: " f"{msg}"
        )
    return success, msg


def import_archived_analysis2(csvfile, year):
    success, msg = import_obj(csvfile, ANALYSIS2_HISTORICAL_KEY, year=year)
    if not success:
        raise WrongChartOFAccountCodeException(
            f"Importing archived Analysis2 (Market) error: " f"{msg}"
        )
    return success, msg
