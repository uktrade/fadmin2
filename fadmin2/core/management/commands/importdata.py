from django.core.management.base import BaseCommand

from costcentre.importcsv import import_cc
# from core.csvimport.treasurysegment import import_treasury_segments
from forecast.importcsv import import_actual
from chartofaccountDIT.importcsv import import_Analysis1, import_Analysis2, \
    import_NAC, import_NAC_expenditure_category, \
    import_NAC_category, import_NAC_DIT_setting, import_NAC_DIT_budget, \
    import_NAC_dashboard_Budget, import_expenditure_category, \
    import_commercial_category, import_commercial_category_responsible, import_programme
from treasuryCOA.importcsv import import_treasury_COA
from payroll.importcsv import import_HR_Report


IMPORT_TYPE = {
    'CostCentre': import_cc,
    # 'Segments' : import_treasury_segments,
    'Treasury_COA': import_treasury_COA,
    'Programmes': import_programme,
    'NAC': import_NAC,  # import from the BICC file
    'Analysis1': import_Analysis1,
    'Analysis2': import_Analysis2,
    'NAC_Dashboard_Group': import_NAC_expenditure_category,
    'NAC_Dashboard_Budget': import_NAC_dashboard_Budget,
    'NAC_Category': import_NAC_category,
    'NAC_DIT_Setting': import_NAC_DIT_setting,  # add extra fields defined by DIT
    'NAC_Budget': import_NAC_DIT_budget,
    'HR_Report': import_HR_Report,
    'NAC_Dashboard_other': import_expenditure_category,
    'Commercial_Cat_responsible': import_commercial_category_responsible,
    'Commercial_Cat': import_commercial_category
}


class Command(BaseCommand):
    help = 'Import CC hierarchy from csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path')
        parser.add_argument('type')
        parser.add_argument('year', type=int, nargs='?', default=None)
        parser.add_argument('month', nargs='?', default=None)

    # pass the file path as an argument
    # second argument will define the content of the file
    # importing actual is a special case, because we need to specify the month
    def handle(self, *args, **options):
        path = options.get('csv_path')
        print(path)
        importtype = options.get('type')
        # Windows-1252 or CP-1252, used because of a back quote
        csvfile = open(path, newline='', encoding='cp1252')
        if importtype == 'Actuals':
            financialyear = options.get('year')
            monthtoimport = options.get('month')
            import_actual(csvfile, financialyear, monthtoimport)
        else:
            IMPORT_TYPE[importtype](csvfile)
        csvfile.close()
