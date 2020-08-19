from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
)

from costcentre.models import HistoricCostCentre


def valid_year_for_archiving_actuals(financial_year):
    # check that the chart of account has been archived.
    # otherwise, every single row of the uploaded file will generate an error
    obj = HistoricCostCentre.filter()
    # User.objects.distinct().filter(widget__in=your_widget_queryset)
    pass