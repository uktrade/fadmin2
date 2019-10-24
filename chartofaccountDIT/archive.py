from core.archive import archive_generic

from .models import (
    Analysis1,
    Analysis2,
    CommercialCategory,
    ExpenditureCategory,
    FCOMapping,
    HistoricalAnalysis1,
    HistoricalAnalysis2,
    HistoricalCommercialCategory,
    HistoricalExpenditureCategory,
    HistoricalFCOMapping,
    HistoricalInterEntity,
    HistoricalNaturalCode,
    HistoricalProgrammeCode,
    HistoricalProjectCode,
    InterEntity,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)


def archive_project_code(year):
    return archive_generic(year, HistoricalProjectCode, ProjectCode)


def archive_programme_code(year):
    return archive_generic(year, HistoricalProgrammeCode, ProgrammeCode)


def archive_expenditure_category(year):
    return archive_generic(year, HistoricalExpenditureCategory, ExpenditureCategory)


def archive_inter_entity(year):
    return archive_generic(year, HistoricalInterEntity, InterEntity)


def archive_fco_mapping(year):
    return archive_generic(year, HistoricalFCOMapping, FCOMapping)


def archive_commercial_category(year):
    return archive_generic(year, HistoricalCommercialCategory, CommercialCategory)


def archive_analysis_1(year):
    return archive_generic(year, HistoricalAnalysis1, Analysis1)


def archive_analysis_2(year):
    return archive_generic(year, HistoricalAnalysis2, Analysis2)


def archive_natural_code(year):
    return archive_generic(year, HistoricalNaturalCode, NaturalCode)


def archive_all(year):
    archive_project_code(year)
    archive_programme_code(year)
    archive_expenditure_category(year)
    archive_inter_entity(year)
    archive_fco_mapping(year)
    archive_commercial_category(year)
    archive_analysis_1(year)
    archive_analysis_2(year)
    archive_natural_code(year)
