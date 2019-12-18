from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import (
    reverse,
)
from django.views.generic.base import TemplateView

from django_tables2 import (
    MultiTableMixin,
)

from costcentre.forms import (
    DirectorateCostCentresForm,
)
from costcentre.models import (
    CostCentre,
    Directorate,
)
from costcentre.models import DepartmentalGroup

from forecast.models import (
    MonthlyFigureAmount,
)
from forecast.tables import (
    ForecastExpandTable,
    ForecastSubTotalTable,
)
from forecast.utils.query_fields import (
    SHOW_COSTCENTRE,
    SHOW_DIRECTORATE,
    SHOW_DIT,
    SHOW_GROUP,
    expenditure_columns,
    expenditure_display_sub_total_column,
    expenditure_order_list,
    expenditure_sub_total, filter_codes,
    filter_selectors,
    hierarchy_columns,
    hierarchy_order_list,
    hierarchy_sub_total,
    hierarchy_sub_total_column,
    programme_columns,
    programme_display_sub_total_column,
    programme_order_list,
    programme_sub_total,
    project_columns,
    project_display_sub_total_column,
    project_order_list,
    project_sub_total,
)
from forecast.views.base import ForecastViewPermissionMixin


class ForecastMultiTableMixin(MultiTableMixin):
    hierarchy_type = -1

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        arg_name = filter_codes[self.hierarchy_type]
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter = {filter_selectors[self.hierarchy_type]: f"{filter_code}"}
        else:
            pivot_filter = {}
        hierarchy_data = MonthlyFigureAmount.pivot.subtotal_data(
            hierarchy_sub_total_column[self.hierarchy_type],
            hierarchy_sub_total,
            hierarchy_columns[self.hierarchy_type].keys(),
            pivot_filter,
            order_list=hierarchy_order_list,
        )
        programme_data = MonthlyFigureAmount.pivot.subtotal_data(
            programme_display_sub_total_column,
            programme_sub_total,
            programme_columns.keys(),
            pivot_filter,
            order_list=programme_order_list,
        )

        expenditure_data = MonthlyFigureAmount.pivot.subtotal_data(
            expenditure_display_sub_total_column,
            expenditure_sub_total,
            expenditure_columns.keys(),
            pivot_filter,
            order_list=expenditure_order_list,
        )

        project_data = MonthlyFigureAmount.pivot.subtotal_data(
            project_display_sub_total_column,
            project_sub_total,
            project_columns.keys(),
            pivot_filter,
            order_list=project_order_list,
        )
        programme_table = ForecastSubTotalTable(programme_columns, programme_data)
        programme_table.attrs['caption'] = "Programme Report"
        expenditure_table = ForecastExpandTable(expenditure_columns, expenditure_data)
        expenditure_table.attrs['caption'] = "Expenditure Report"
        project_table = ForecastSubTotalTable(project_columns, project_data)
        project_table.attrs['caption'] = "Project Report"

        self.tables = [
            # ForecastSubTotalTable(
            #     hierarchy_columns[self.hierarchy_type],
            #     hierarchy_data),
            # programme_table,
            expenditure_table,
            # project_table,
        ]
        return self.tables


class DITView(
    ForecastViewPermissionMixin,
    ForecastMultiTableMixin,
    TemplateView,
):
    template_name = "forecast/view/dit.html"
    table_pagination = False
    hierarchy_type = SHOW_DIT

    def groups(self):
        return DepartmentalGroup.objects.filter(
            active=True,
        )


class GroupView(
    ForecastViewPermissionMixin,
    ForecastMultiTableMixin,
    TemplateView,
):
    template_name = "forecast/view/group.html"
    table_pagination = False
    hierarchy_type = SHOW_GROUP

    def group(self):
        return DepartmentalGroup.objects.get(
            group_code=self.kwargs['group_code'],
            active=True,
        )

    def directorates(self):
        return Directorate.objects.filter(
            group__group_code=self.kwargs['group_code'],
            active=True,
        )


class DirectorateView(
    ForecastViewPermissionMixin,
    ForecastMultiTableMixin,
    TemplateView,
):
    template_name = "forecast/view/directorate.html"
    table_pagination = False
    hierarchy_type = SHOW_DIRECTORATE

    def directorate(self):
        return Directorate.objects.get(
            directorate_code=self.kwargs['directorate_code'],
            active=True,
        )

    def cost_centres_form(self):
        return DirectorateCostCentresForm(
            directorate_code=self.kwargs['directorate_code']
        )

    def post(self, request, *args, **kwargs):
        cost_centre_code = request.POST.get(
            'cost_centre',
            None,
        )
        if cost_centre_code:
            return HttpResponseRedirect(
                reverse(
                    "forecast_cost_centre",
                    kwargs={'cost_centre_code': cost_centre_code}
                )
            )
        else:
            raise Http404("Cost Centre not found")


class CostCentreView(
    ForecastViewPermissionMixin,
    ForecastMultiTableMixin,
    TemplateView,
):
    template_name = "forecast/view/cost_centre.html"
    table_pagination = False
    hierarchy_type = SHOW_COSTCENTRE

    def cost_centre(self):
        return CostCentre.objects.get(
            cost_centre_code=self.kwargs[filter_codes[self.hierarchy_type]],
        )

    def cost_centres_form(self):
        cost_centre = self.cost_centre()

        return DirectorateCostCentresForm(
            directorate_code=cost_centre.directorate.directorate_code
        )

    def post(self, request, *args, **kwargs):
        cost_centre_code = request.POST.get(
            'cost_centre',
            None,
        )
        if cost_centre_code:
            return HttpResponseRedirect(
                reverse(
                    "forecast_cost_centre",
                    kwargs={'cost_centre_code': cost_centre_code}
                )
            )
        else:
            raise Http404("Cost Centre not found")


