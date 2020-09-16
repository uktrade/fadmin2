import csv

from chartofaccountDIT.models import (
    ArchivedAnalysis1,
)

from core.import_csv import (
    IMPORT_CSV_FIELDLIST_KEY,
    IMPORT_CSV_IS_FK,
    IMPORT_CSV_MODEL_KEY,
    IMPORT_CSV_PK_KEY,
    IMPORT_CSV_PK_NAME_KEY,
    ImportInfo,
    csv_header_to_dict,
    import_list_obj,
    import_obj,
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


def import_archived_analysis1(csvfile, year):
    return import_obj(csvfile, ANALYSIS1_HISTORICAL_KEY, year = year)




