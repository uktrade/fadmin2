
from django_tables2.views import SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from django_tables2 import RequestConfig

from .models import NACCategory, NaturalCode, Analysis1, Analysis2, NACDashboardGrouping

from .tables import NaturalCodeTable
from .filters import NACFilter


class FilteredNACListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = NaturalCodeTable
    model = NaturalCode
    paginate_by = 50
    template_name = 'core/table_filter_generic.html'
    filterset_class = NACFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Natural Account Codes (NAC)'
        return context

