from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse
from django.views.generic.base import TemplateView

from django_tables2 import MultiTableMixin

from costcentre.forms import DirectorateCostCentresForm
from costcentre.models import (
    CostCentre,
    Directorate,
)
from costcentre.models import DepartmentalGroup

from forecast.models import (
    FinancialPeriod,
    ForecastingDataView,
)
from forecast.tables import (
    ForecastSubTotalTable,
    ForecastWithLinkTable,
)
from forecast.utils.query_fields import (
    BUDGET_CATEGORY_ID,
    BUDGET_CATEGORY_NAME,
    BUDGET_TYPE,
    FORECAST_EXPENDITURE_TYPE_NAME,
    PROGRAMME_CODE,
    PROGRAMME_NAME,
    PROJECT_CODE,
    PROJECT_NAME,
    SHOW_COSTCENTRE,
    SHOW_DIRECTORATE,
    SHOW_DIT,
    SHOW_GROUP,
    expenditure_columns,
    expenditure_display_sub_total_column,
    expenditure_order_list,
    expenditure_sub_total,
    expenditure_view,
    filter_codes,
    filter_selectors,
    hierarchy_columns,
    hierarchy_order_list,
    hierarchy_sub_total,
    hierarchy_sub_total_column,
    hierarchy_view,
    hierarchy_view_code,
    hierarchy_view_link_column,
    programme_columns,
    programme_detail_view,
    programme_display_sub_total_column,
    programme_order_list,
    programme_sub_total,
    project_columns,
    project_detail_view,
    project_display_sub_total_column,
    project_order_list,
    project_sub_total,
)
from forecast.views.base import ForecastViewPermissionMixin

class PeriodTableViewMixin(MultiTableMixin):

    def __init__(self, *args, **kwargs):
        self._period = None
        self._month_list = None
        self._datamodel = None
        self._table_tag = None

        super().__init__(*args, **kwargs)

    def get_period(self):
        if self._period is None:
            self._period = self.kwargs["period"]
        return self._period

    def get_month_list(self):
        if self._month_list is None:
            period = self.get_period()
            if period:
                # We are displaying historical forecast
                self._month_list = FinancialPeriod.financial_period_info.month_sublist(
                    period)
            else:
                self._month_list = FinancialPeriod.financial_period_info.actual_month_list()
        return self._month_list

    def get_datamodel(self):
        if self._datamodel is None:
            period = self.get_period()
            if period:
                # We are displaying historical forecast
                self._datamodel = ForecastingDataView
            else:
                 self._datamodel = ForecastingDataView
        return self._datamodel

    def get_table_tag(self):
        if self._table_tag is None:
            period = self.get_period()
            if period:
                # We are displaying historical forecast
                forecast_period_obj = FinancialPeriod.objects.get(pk=period)
                self._table_tag  = f'Historical data for {forecast_period_obj.period_long_name}'
            else:
                self._table_tag = ""
        return self._table_tag



class ForecastMultiTableMixin(PeriodTableViewMixin):
    hierarchy_type = -1

    def class_name(self):
        return "wide-table"

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        filter_code = ""
        pivot_filter = {}
        arg_name = filter_codes[self.hierarchy_type]
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter = {filter_selectors[self.hierarchy_type]: f"{filter_code}"}
        datamodel = self.get_datamodel()
        period = self.get_period()
        table_tag = self.get_table_tag()
        month_list = self.get_month_list()

        hierarchy_data = datamodel.view_data.subtotal_data(
            hierarchy_sub_total_column[self.hierarchy_type],
            hierarchy_sub_total,
            hierarchy_columns[self.hierarchy_type].keys(),
            pivot_filter,
            order_list=hierarchy_order_list,
        )
        programme_data = datamodel.view_data.subtotal_data(
            programme_display_sub_total_column,
            programme_sub_total,
            programme_columns.keys(),
            pivot_filter,
            order_list=programme_order_list,
        )

        expenditure_data = datamodel.view_data.subtotal_data(
            expenditure_display_sub_total_column,
            expenditure_sub_total,
            expenditure_columns.keys(),
            pivot_filter,
            order_list=expenditure_order_list,
        )

        # In the project report, exclude rows without a project code.
        k = f"{PROJECT_CODE}__isnull"
        pivot_filter.update({k: False})
        project_data = datamodel.view_data.subtotal_data(
            project_display_sub_total_column,
            project_sub_total,
            project_columns.keys(),
            pivot_filter,
            order_list=project_order_list,
        )

        if self.hierarchy_type == SHOW_COSTCENTRE:
            programme_table = ForecastSubTotalTable(
                programme_columns,
                programme_data,
                actual_month_list=month_list,
            )
        else:
            programme_table = ForecastWithLinkTable(
                PROGRAMME_NAME,
                programme_detail_view[self.hierarchy_type],
                [PROGRAMME_CODE, FORECAST_EXPENDITURE_TYPE_NAME, period],
                filter_code,
                programme_columns,
                programme_data,
                actual_month_list=month_list,
            )

        programme_table.attrs['caption'] = "Control total report"
        programme_table.tag = table_tag

        expenditure_table = ForecastWithLinkTable(
            BUDGET_CATEGORY_NAME,
            expenditure_view[self.hierarchy_type],
            [BUDGET_CATEGORY_ID, BUDGET_TYPE, period],
            filter_code,
            expenditure_columns,
            expenditure_data,
            actual_month_list=month_list,
        )
        expenditure_table.attrs['caption'] = "Expenditure report"
        expenditure_table.tag = table_tag

        project_table = ForecastWithLinkTable(
            PROJECT_NAME,
            project_detail_view[self.hierarchy_type],
            [PROJECT_CODE, period],
            filter_code,
            project_columns,
            project_data,
            actual_month_list=month_list,
        )
        project_table.attrs['caption'] = "Project report"
        project_table.tag = table_tag

        if self.hierarchy_type == SHOW_COSTCENTRE:
            hierarchy_table = ForecastSubTotalTable(
                hierarchy_columns[self.hierarchy_type],
                hierarchy_data,
                actual_month_list=month_list,
            )
        else:
            hierarchy_table = ForecastWithLinkTable(
                hierarchy_view_link_column[self.hierarchy_type],
                hierarchy_view[self.hierarchy_type],
                [hierarchy_view_code[self.hierarchy_type], period],
                "",
                hierarchy_columns[self.hierarchy_type],
                hierarchy_data,
                actual_month_list=month_list,
            )

        hierarchy_table.attrs['caption'] = "Forecast hierarchy report"
        hierarchy_table.tag = table_tag

        self.tables = [
            hierarchy_table,
            programme_table,
            expenditure_table,
            project_table,
        ]

        return self.tables


class DITView(
    ForecastViewPermissionMixin, ForecastMultiTableMixin, TemplateView
):
    template_name = "forecast/view/dit.html"
    table_pagination = False
    hierarchy_type = SHOW_DIT


class GroupView(
    ForecastViewPermissionMixin, ForecastMultiTableMixin, TemplateView,
):
    template_name = "forecast/view/group.html"
    table_pagination = False
    hierarchy_type = SHOW_GROUP

    def group(self):
        return DepartmentalGroup.objects.get(
            group_code=self.kwargs["group_code"], active=True,
        )


class DirectorateView(
    ForecastViewPermissionMixin, ForecastMultiTableMixin, TemplateView,
):
    template_name = "forecast/view/directorate.html"
    table_pagination = False
    hierarchy_type = SHOW_DIRECTORATE

    def directorate(self):
        return Directorate.objects.get(
            directorate_code=self.kwargs["directorate_code"], active=True,
        )

    def cost_centres_form(self):
        return DirectorateCostCentresForm(
            directorate_code=self.kwargs["directorate_code"]
        )


class CostCentreView(
    ForecastViewPermissionMixin, ForecastMultiTableMixin, TemplateView
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
        cost_centre_code = request.POST.get("cost_centre", None,)
        if cost_centre_code:
            return HttpResponseRedirect(
                reverse(
                    "forecast_cost_centre",
                    kwargs={
                            "cost_centre_code": cost_centre_code,
                            "period": self.get_period(),
                    },
                )
            )
        else:
            raise Http404("Cost Centre not found")
