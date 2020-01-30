from core.archive import archive_generic

from .models import (
    Analysis1,
    Analysis2,
    ArchiveAnalysis1,
    ArchiveAnalysis2,
    ArchiveCommercialCategory,
    ArchiveExpenditureCategory,
    ArchiveFCOMapping,
    ArchiveInterEntity,
    ArchiveNaturalCode,
    ArchiveProgrammeCode,
    ArchiveProjectCode,
    CommercialCategory,
    ExpenditureCategory,
    FCOMapping,
    InterEntity,
    NaturalCode,
    ProgrammeCode,
    ProjectCode,
)


def archive_project_code(year):
    return archive_generic(year, ArchiveProjectCode, ProjectCode)


def archive_programme_code(year):
    return archive_generic(year, ArchiveProgrammeCode, ProgrammeCode)


def archive_expenditure_category(year):
    return archive_generic(year, ArchiveExpenditureCategory, ExpenditureCategory)


def archive_inter_entity(year):
    return archive_generic(year, ArchiveInterEntity, InterEntity)


def archive_fco_mapping(year):
    return archive_generic(year, ArchiveFCOMapping, FCOMapping)


def archive_commercial_category(year):
    return archive_generic(year, ArchiveCommercialCategory, CommercialCategory)


def archive_analysis_1(year):
    return archive_generic(year, ArchiveAnalysis1, Analysis1)


def archive_analysis_2(year):
    return archive_generic(year, ArchiveAnalysis2, Analysis2)


def archive_natural_code(year):
    return archive_generic(year, ArchiveNaturalCode, NaturalCode)


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
