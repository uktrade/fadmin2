from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse

from chartofaccountDIT.forms import ExpenditureTypeForm

from forecast.tables import ForecastSubTotalTable
from forecast.utils.query_fields import (
    SHOW_COSTCENTRE,
    SHOW_DIRECTORATE,
    SHOW_DIT,
    SHOW_GROUP,
)
from forecast.views.base import (
    ForecastViewPermissionMixin,
    ForecastViewTableMixin,
    PeriodView,
)


class ForecastExpenditureDetailsMixin(ForecastViewTableMixin):
    hierarchy_type = -1
    table_pagination = False

    def class_name(self):
        return "wide-table"

    def expenditure_category(self):
        return self.field_infos.\
            expenditure_category(self.kwargs["expenditure_category"],)

    def budget_type(self):
        return self.kwargs["budget_type"]

    def expenditure_type_form(self):
        return ExpenditureTypeForm(
            expenditure_category=self.kwargs["expenditure_category"],
            year=self.year
        )

    def post(self, request, *args, **kwargs):
        self.selected_period = request.POST.get("selected_period", None,)
        if self.selected_period is None:
            self.selected_period = self.period
            # Check that an expenditure category was selected
            self.selected_expenditure_category_id = request.POST.get(
                "expenditure_category", None,
            )
            if self.selected_expenditure_category_id is None:
                raise Http404("Budget Type not found")
        else:
            self.selected_expenditure_category_id = self.kwargs["expenditure_category"]
        return HttpResponseRedirect(
            reverse(self.url_name, kwargs=self.selection_kwargs(),)
        )

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        budget_type_id = self.kwargs["budget_type"]
        expenditure_category_id = self.kwargs["expenditure_category"]
        pivot_filter = {
            self.field_infos.budget_category_id_field: f"{expenditure_category_id}",
            self.field_infos.budget_type_field: f"{budget_type_id}",
        }
        self.field_infos.hierarchy_type = self.hierarchy_type
        arg_name = self.field_infos.filter_codes
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter[self.field_infos.filter_selector] = f"{filter_code}"

        nac_data = self.data_model.view_data.subtotal_data(
            self.field_infos.nac_display_sub_total_column,
            self.field_infos.nac_sub_total,
            self.field_infos.nac_columns.keys(),
            pivot_filter,
            order_list=self.field_infos.nac_order_list,
            show_grand_total=False,
        )

        nac_table = ForecastSubTotalTable(
            self.field_infos.nac_columns, nac_data, actual_month_list=self.month_list,
        )
        nac_table.attrs["caption"] = "Expenditure Report"
        nac_table.tag = self.table_tag
        self.tables = [
            nac_table,
        ]
        return self.tables


class DITExpenditureDetailsView(
    ForecastViewPermissionMixin, ForecastExpenditureDetailsMixin, PeriodView,
):
    template_name = "forecast/view/expenditure_details/dit.html"
    hierarchy_type = SHOW_DIT
    url_name = "expenditure_details_dit"

    def selection_kwargs(self):
        return {
            "expenditure_category": self.selected_expenditure_category_id,
            "budget_type": self.budget_type(),
            "period": self.selected_period,
        }


class GroupExpenditureDetailsView(
    ForecastViewPermissionMixin, ForecastExpenditureDetailsMixin, PeriodView,
):
    template_name = "forecast/view/expenditure_details/group.html"
    hierarchy_type = SHOW_GROUP
    url_name = "expenditure_details_group"

    def group(self):
        return self.field_infos.group(self.kwargs["group_code"])

    def selection_kwargs(self):
        return {
            "group_code": self.kwargs["group_code"],
            "expenditure_category": self.selected_expenditure_category_id,
            "budget_type": self.budget_type(),
            "period": self.selected_period,
        }


class DirectorateExpenditureDetailsView(
    ForecastViewPermissionMixin, ForecastExpenditureDetailsMixin, PeriodView,
):
    template_name = "forecast/view/expenditure_details/directorate.html"
    hierarchy_type = SHOW_DIRECTORATE
    url_name = "expenditure_details_directorate"

    def directorate(self):
        return self.field_infos.directorate(self.kwargs["directorate_code"])

    def selection_kwargs(self):
        return {
            "directorate_code": self.kwargs["directorate_code"],
            "expenditure_category": self.selected_expenditure_category_id,
            "budget_type": self.budget_type(),
            "period": self.selected_period,
        }


class CostCentreExpenditureDetailsView(
    ForecastViewPermissionMixin, ForecastExpenditureDetailsMixin, PeriodView,
):
    template_name = "forecast/view/expenditure_details/cost_centre.html"
    table_pagination = False
    hierarchy_type = SHOW_COSTCENTRE
    url_name = "expenditure_details_cost_centre"

    def cost_centre(self):
        return self.field_infos.cost_centre(self.kwargs["cost_centre_code"])

    def selection_kwargs(self):
        return {
            "cost_centre_code": self.kwargs["cost_centre_code"],
            "expenditure_category": self.selected_expenditure_category_id,
            "budget_type": self.budget_type(),
            "period": self.selected_period,
        }
