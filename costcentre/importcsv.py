import csv

from core.importcsv import IMPORT_CSV_FIELDLIST_KEY, IMPORT_CSV_MODEL_KEY, IMPORT_CSV_PK_KEY, \
    ImportInfo, convert_to_bool_string, csvheadertodict, import_obj

from .models import BSCEEmail, BusinessPartner, \
    CostCentre, CostCentrePerson, DepartmentalGroup, Directorate

# define the column position in the csv file.

# COLUMN_KEY = {
#                 'GroupCode': 3,
#                 'GroupName': 4,
#                 'DirectorateCode': 5,
#                 'DirectorateName': 6,
#                 'CCCode': 7,
#                 'CCName': 8}
#
#
# def importcostcentres(csvfile):
#     csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#     for row in csvreader:
#         # Create DG Group, Directorate and Cost centre
#         objDG, created = DepartmentalGroup.objects.update_or_create(
#             GroupCode=row[COLUMN_KEY['GroupCode']],
#             defaults={'GroupName': row[COLUMN_KEY['GroupName']]},
#         )
#         objdir, created = Directorate.objects.update_or_create(
#             DirectorateCode=row[COLUMN_KEY['DirectorateCode']],
#             defaults={'GroupCode': objDG,
#                        'DirectorateName':row[COLUMN_KEY['DirectorateName']]},
#         )
#         obj, created = CostCentre.objects.update_or_create(
#             CCCode=row[COLUMN_KEY['CCCode']],
#             defaults={CostCentre.CCName.field_name: row[COLUMN_KEY['CCName']],
#                       CostCentre.Directorate.field.name: objdir},
#         )
#

GROUP_KEY = {IMPORT_CSV_MODEL_KEY: DepartmentalGroup,
             IMPORT_CSV_PK_KEY: 'Group Code',
             'fieldlist': {DepartmentalGroup.group_name.field_name: 'Group Description'}}

DIR_KEY = {IMPORT_CSV_MODEL_KEY: Directorate,
           IMPORT_CSV_PK_KEY: 'Directorate Code',
           IMPORT_CSV_FIELDLIST_KEY:
               {Directorate.directorate_name.field_name: 'Directorate Description',
                Directorate.group.field.name: GROUP_KEY}}

CC_KEY = {IMPORT_CSV_MODEL_KEY: CostCentre,
          IMPORT_CSV_PK_KEY: 'Cost Centre',
          IMPORT_CSV_FIELDLIST_KEY: {CostCentre.cost_centre_name.field_name: 'Cost Centre Description',
                                     CostCentre.active.field_name: 'Active',
                                     CostCentre.directorate.field.name: DIR_KEY}}


def import_cc(csvfile):
    import_obj(csvfile, CC_KEY)


import_cc_class = ImportInfo(CC_KEY, 'Departmental Groups, Directorates and Cost Centres')


def import_cc_dit_specific(csvfile):
    """Special function to import the Deputy Director,  Business partner and BSCE email"""
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csvheadertodict(next(reader))
    for row in reader:
        obj = CostCentre.objects.get(
            pk=row[header['cost centre']].strip())
        temp = row[header['deputy name']].strip()
        if temp != '':
            deputy_obj, created = CostCentrePerson.objects.get_or_create(
                name=row[header['deputy name']].strip(),
                surname=row[header['deputy surname']].strip())
            deputy_obj.email = row[header['deputy email']].strip()
            deputy_obj.active = True
            deputy_obj.save()
            obj.deputy_director = deputy_obj
        else:
            obj.deputy_director = None
        temp = row[header['bp name']].strip()
        if temp != '':
            bp_obj, created = BusinessPartner.objects.get_or_create(
                name=row[header['bp name']].strip(),
                surname=row[header['bp surname']].strip())
            bp_obj.bp_email = row[header['bp email']].strip()
            bp_obj.active = True
            bp_obj.save()
            obj.business_partner = bp_obj
        else:
            obj.business_partner = None
        temp = row[header['bsce email']].strip()
        if temp != '':
            bsce_obj, created = BSCEEmail.objects.get_or_create(
                bsce_email=row[header['bsce email']].strip())
            obj.bsce_email = bsce_obj
        else:
            obj.bsce_email = None
        obj.disabled_with_actual = convert_to_bool_string(
            row[header['disabled (actuals to be cleared)']].strip())
        obj.active = convert_to_bool_string(row[header['active']].strip())
        obj.used_for_travel = convert_to_bool_string(row[header['used for travel']].strip())
        obj.save()


import_cc_dit_specific_class = ImportInfo({}, 'DIT Information',
                                          ['Cost Centre',
                                           'BP Name', 'BP Surname', 'BP Email',
                                           'Deputy Name', 'Deputy Surname', 'Deputy Email',
                                           'BSCE Email', 'Active',
                                           'Disabled (Actuals to be cleared)', 'Used for Travel'],
                                          import_cc_dit_specific)


def import_director(csvfile):
    """Special function to import Groups with the DG, because I need to change the people
    during the import"""
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csvheadertodict(next(reader))
    for row in reader:
        obj = Directorate.objects.get(
            pk=row[header['Directorate Code']].strip())
        director_obj, created = CostCentrePerson.objects.get_or_create(
            name=row[header['Director Name']].strip(),
            surname=row[header['Director Surname']].strip())
        director_obj.email = row[header['Director email']].strip()
        director_obj.active = True
        director_obj.is_director = True
        director_obj.save()
        obj.director = director_obj
        obj.save()


import_director_class = ImportInfo({}, 'Directors',
                                   ['Directorate Code',
                                    'Directorate Name', 'Directorate Surname',
                                    'Directorate Email'],
                                   import_director)


def import_group_with_dg(csvfile):
    """Special function to import Groups with the DG, because I need to change the people
    during the import"""
    reader = csv.reader(csvfile)
    # Convert the first row to a dictionary of positions
    header = csvheadertodict(next(reader))
    for row in reader:
        obj = DepartmentalGroup.objects.get(
            pk=row[header['Group Code']].strip())
        dg_obj, created = CostCentrePerson.objects.get_or_create(
            name=row[header['DG Name']].strip(),
            surname=row[header['DG Surname']].strip())
        dg_obj.email = row[header['DG email']].strip()
        dg_obj.active = True
        dg_obj.is_dg = True
        dg_obj.save()
        obj.director_general = dg_obj
        obj.save()


import_departmental_group_class = ImportInfo({}, 'Director Generals',
                                             ['Group Code',
                                              'DG Name', 'DG Surname',
                                              'DG email'],
                                             import_group_with_dg)