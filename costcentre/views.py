from core.views import FAdminFilteredView

from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import CostCentreFilter
from .tables import CostCentreTable


class FilteredCostListView(LoginRequiredMixin, FAdminFilteredView):
    table_class = CostCentreTable
    model = table_class.Meta.model
    filterset_class = CostCentreFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Cost Centre Hierarchy'
        return context
