# from core.import_csv import (
#     IMPORT_CSV_FIELDLIST_KEY,
#     IMPORT_CSV_IS_FK,
#     IMPORT_CSV_MODEL_KEY,
#     IMPORT_CSV_PK_KEY,
#     ImportInfo,
#     import_obj,
# )
#
#
# from costcentre.models import CostCentre, DepartmentalGroup, Directorate
#
# from gifthospitality.models import DITGroup
#
# from .models import DITPeople, Grade
#
# GRADE_KEY = {
#     IMPORT_CSV_MODEL_KEY: Grade,
#     IMPORT_CSV_PK_KEY: "Grade",
#     IMPORT_CSV_FIELDLIST_KEY: {Grade.gradedescription.field_name: "Grade Description"},
# }
#
# import_grade_class = ImportInfo(GRADE_KEY)
#
# # GRADE_KEY = {
# #     IMPORT_CSV_MODEL_KEY: Grade,
# #     IMPORT_CSV_IS_FK: "",
# #     IMPORT_CSV_PK_KEY: "Grade",
# # }
#
# CC_FK_KEY = {
#     IMPORT_CSV_MODEL_KEY: CostCentre,
#     IMPORT_CSV_IS_FK: "",
#     IMPORT_CSV_PK_KEY: "CC",
# }
#
# GC_FK_KEY = {
#     IMPORT_CSV_MODEL_KEY: DepartmentalGroup,
#     IMPORT_CSV_IS_FK: "",
#     IMPORT_CSV_PK_KEY: "GC",
# }
#
# DC_FK_KEY = {
#     IMPORT_CSV_MODEL_KEY: Directorate,
#     IMPORT_CSV_IS_FK: "",
#     IMPORT_CSV_PK_KEY: "DC",
# }
#
# PEOPLE_KEY = {
#     IMPORT_CSV_MODEL_KEY: DITPeople,
#     IMPORT_CSV_PK_KEY: "SE-No",
#     IMPORT_CSV_FIELDLIST_KEY: {
#         DITPeople.surname.field_name: "Last Name",
#         DITPeople.name.field_name: "First Name",
#         DITPeople.grade.field.name: GRADE_KEY,
#         DITPeople.cost_centre.field.name: CC_FK_KEY,
#     },
# }
#
# GROUP_KEY = {
#     IMPORT_CSV_MODEL_KEY: DITGroup,
#     IMPORT_CSV_PK_KEY: "SE-No",
#     IMPORT_CSV_FIELDLIST_KEY: {
#         DITGroup.group_display_name.field_name: "Group Name",
#         DITGroup.cost_centre.field.name: CC_FK_KEY,
#         DITGroup.directorate_code.field.name: DC_FK_KEY,
#         DITGroup.group_code.field.name: GC_FK_KEY,
#     }
# }
#
#
# def import_HR_Report(csvfile):
#     import_obj(csvfile, PEOPLE_KEY)
#
#
# def import_GROUP_Report(csvfile):
#     import_obj(csvfile, GROUP_KEY)
#
#
# import_HR_class = ImportInfo(PEOPLE_KEY)
#
# import_GROUP_class = ImportInfo(GROUP_KEY)
