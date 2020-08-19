from core.models import FinancialYear

def valid_year_for_archiving_actuals(financial_year):
    # check that the chart of account has been archived.
    # otherwise, every single row of the uploaded file will generate an error
    try:
        obj = FinancialYear.object.get(pk=financial_year)
    except FinancialYear.DoesNotExist:
        return False

    # Checks if there are cost centres archived for this year
    # and all the members of the Chart of Account
    if  obj.previous_years_archivedfinancialcode_financial_year.all().count() & \
        obj.chartofaccountdit_archivednaturalcode_financial_year.all().count() & \
        obj.chartofaccountdit_archivedanalysis1_financial_year.all().count() & \
        obj.chartofaccountdit_archivedanalysis2_financial_year.all().count() & \
        obj.chartofaccountdit_archivedprogrammecode_financial_year.all().count() & \
        obj.chartofaccountdit_archivedprojectcode_financial_year.all().count():
        return True
    return False
