from core.import_csv import (
    IMPORT_CSV_FIELDLIST_KEY,
    IMPORT_CSV_IS_FK,
    IMPORT_CSV_MODEL_KEY,
    IMPORT_CSV_PK_KEY,
    IMPORT_CSV_PK_NAME_KEY,
    ImportInfo,
)

from gifthospitality.models import (
    GiftAndHospitality,
    GiftAndHospitalityCategory,
    GiftAndHospitalityClassification,
    GiftAndHospitalityCompany,
    Grade,
)

GH_CLASSIF_KEY = {
    IMPORT_CSV_MODEL_KEY: GiftAndHospitalityClassification,
    IMPORT_CSV_PK_NAME_KEY: GiftAndHospitalityClassification.gif_hospitality_classification,  # noqa
    IMPORT_CSV_PK_KEY: "Classification",
    IMPORT_CSV_FIELDLIST_KEY: {
        GiftAndHospitalityClassification.gift_type,
        GiftAndHospitalityClassification.sequence_no,
    },
}

import_gh_classification_class = ImportInfo(GH_CLASSIF_KEY)

GH_COMPANY_KEY = {
    IMPORT_CSV_MODEL_KEY: GiftAndHospitalityCompany,
    IMPORT_CSV_PK_KEY: "Company",
    IMPORT_CSV_PK_NAME_KEY: GiftAndHospitalityCompany.gif_hospitality_company,  # noqa
    IMPORT_CSV_FIELDLIST_KEY: {
        GiftAndHospitalityCompany.sequence_no: "sequence_no"
    },
}

import_gh_company_class = ImportInfo(GH_COMPANY_KEY)

GH_CATEGORY_KEY = {
    IMPORT_CSV_MODEL_KEY: GiftAndHospitalityCategory,
    IMPORT_CSV_PK_KEY: "Category",
    IMPORT_CSV_PK_NAME_KEY: GiftAndHospitalityCategory.gif_hospitality_category,  # noqa
    IMPORT_CSV_FIELDLIST_KEY: {
        GiftAndHospitalityCategory.sequence_no: "sequence_no"
    },
}

import_gh_category_class = ImportInfo(GH_CATEGORY_KEY)

GH_CAT_FK_KEY = {
    IMPORT_CSV_MODEL_KEY: GiftAndHospitalityCategory,
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_KEY: "Category",
    IMPORT_CSV_PK_NAME_KEY: GiftAndHospitalityCategory.gif_hospitality_category,  # noqa
}

GH_CLASS_FK_KEY = {
    IMPORT_CSV_MODEL_KEY: GiftAndHospitalityClassification,
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_KEY: "Type",
    IMPORT_CSV_PK_NAME_KEY: GiftAndHospitalityClassification.gif_hospitality_classification,  # noqa
}

GH_GRADE_KEY = {
    IMPORT_CSV_MODEL_KEY: Grade,
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_KEY: "Grade",
}

import_grade_class = ImportInfo(GH_GRADE_KEY)

"""
NB: Commented code below may be required at a later date subject to client's request
"""
GH_KEY = {
    IMPORT_CSV_MODEL_KEY: GiftAndHospitality,
    IMPORT_CSV_FIELDLIST_KEY: {
        GiftAndHospitality.old_id: "HospID",
        GiftAndHospitality.classification: GH_CLASS_FK_KEY,
        GiftAndHospitality.group_name: "Group",
        GiftAndHospitality.date_agreed: "Date of event/gift offered",
        GiftAndHospitality.venue: "Venue",
        GiftAndHospitality.reason: "Description of offer & reason",
        GiftAndHospitality.value: "Estimate value of offer",
        # GiftAndHospitality.group.field_name: "DIT group offered to/from",
        GiftAndHospitality.rep: "DIT representative offered to/from",
        GiftAndHospitality.offer: "Offer",
        GiftAndHospitality.company_rep: "Company representative offered to/from",  # noqa
        # GiftAndHospitality.company.field_name: "Company offered to/from",
        # GiftAndHospitality.company_name.field_name: "Other Company",
        GiftAndHospitality.action_taken: "Action taken",
        GiftAndHospitality.entered_by: "Entered By",
        GiftAndHospitality.entered_date_stamp: "Date Entered",
        GiftAndHospitality.category: GH_CAT_FK_KEY,
        GiftAndHospitality.grade: GH_GRADE_KEY,
    },
}

import_gh_class = ImportInfo(GH_KEY)
