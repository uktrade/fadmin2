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
    IMPORT_CSV_PK_NAME_KEY: GiftAndHospitalityClassification.gif_hospitality_classification.field_name,  # noqa
    IMPORT_CSV_PK_KEY: "Classification",
    IMPORT_CSV_FIELDLIST_KEY: {
        GiftAndHospitalityClassification.gift_type.field_name: "Type",
        GiftAndHospitalityClassification.sequence_no.field_name: "sequence_no",
    },
}

import_gh_classification_class = ImportInfo(GH_CLASSIF_KEY)

GH_COMPANY_KEY = {
    IMPORT_CSV_MODEL_KEY: GiftAndHospitalityCompany,
    IMPORT_CSV_PK_KEY: "Company",
    IMPORT_CSV_PK_NAME_KEY: GiftAndHospitalityCompany.gif_hospitality_company.field_name,  # noqa
    IMPORT_CSV_FIELDLIST_KEY: {
        GiftAndHospitalityCompany.sequence_no.field_name: "sequence_no"
    },
}

import_gh_company_class = ImportInfo(GH_COMPANY_KEY)

GH_CATEGORY_KEY = {
    IMPORT_CSV_MODEL_KEY: GiftAndHospitalityCategory,
    IMPORT_CSV_PK_KEY: "Category",
    IMPORT_CSV_PK_NAME_KEY: GiftAndHospitalityCategory.gif_hospitality_category.field_name,  # noqa
    IMPORT_CSV_FIELDLIST_KEY: {
        GiftAndHospitalityCategory.sequence_no.field_name: "sequence_no"
    },
}

import_gh_category_class = ImportInfo(GH_CATEGORY_KEY)

GH_CAT_FK_KEY = {
    IMPORT_CSV_MODEL_KEY: GiftAndHospitalityCategory,
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_KEY: "Category",
    IMPORT_CSV_PK_NAME_KEY: GiftAndHospitalityCategory.gif_hospitality_category.field_name,  # noqa
}

GH_CLASS_FK_KEY = {
    IMPORT_CSV_MODEL_KEY: GiftAndHospitalityClassification,
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_KEY: "Type",
    IMPORT_CSV_PK_NAME_KEY: GiftAndHospitalityClassification.gif_hospitality_classification.field_name,  # noqa
}

GH_GRADE_KEY = {
    IMPORT_CSV_MODEL_KEY: Grade,
    IMPORT_CSV_IS_FK: "",
    IMPORT_CSV_PK_KEY: "Grade",
}

GH_KEY = {
    IMPORT_CSV_MODEL_KEY: GiftAndHospitality,
    IMPORT_CSV_FIELDLIST_KEY: {
        GiftAndHospitality.old_id.field_name: "HospID",
        GiftAndHospitality.classification.field.name: GH_CLASS_FK_KEY,
        GiftAndHospitality.group_name.field_name: "Group",
        GiftAndHospitality.date_offered.field_name: "Date of event/gift offered",
        GiftAndHospitality.venue.field_name: "Venue",
        GiftAndHospitality.reason.field_name: "Description of offer & reason",
        GiftAndHospitality.value.field_name: "Estimate value of offer",
        # GiftAndHospitality.group.field_name: "DIT group offered to/from",
        GiftAndHospitality.rep.field_name: "DIT representative offered to/from",
        GiftAndHospitality.offer.field_name: "Offer",
        GiftAndHospitality.company_rep.field_name: "Company representative offered to/from",  # noqa
        # GiftAndHospitality.company.field_name: "Company offered to/from",
        GiftAndHospitality.action_taken.field_name: "Action taken",
        GiftAndHospitality.entered_by.field_name: "Entered By",
        GiftAndHospitality.entered_date_stamp.field_name: "Date Entered",
        GiftAndHospitality.category.field.name: GH_CAT_FK_KEY,
        GiftAndHospitality.grade.field.name: GH_GRADE_KEY,
    },
}

import_gh_class = ImportInfo(GH_KEY)
