from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import (
    reverse,
)
from django.views.generic.base import TemplateView

from django_tables2 import (
    MultiTableMixin,
)

from chartofaccountDIT.forms import (
    ProgrammeForm,
)
from chartofaccountDIT.models import ProgrammeCode

from costcentre.models import (
    CostCentre,
    Directorate,
)
from costcentre.models import DepartmentalGroup

from forecast.models import (
    MonthlyFigureAmount,
)
from forecast.tables import (
    ForecastSubTotalTable,
)
from forecast.utils.query_fields import (
    FORECAST_EXPENDITURE_TYPE_ID,
    PROGRAMME_CODE,
    SHOW_COSTCENTRE,
    SHOW_DIRECTORATE,
    SHOW_DIT,
    SHOW_GROUP,
    filter_codes,
    filter_selectors,
    nac_columns,
    programme_details_hierarchy_columns,
    programme_details_display_sub_total_column,
    programme_details_dit_columns,
    programme_details_directorate_columns,
    programme_details_group_columns,
    programme_details_order_list,
    programme_details_sub_total,
)
from forecast.views.base import ForecastViewPermissionMixin


class ForecastProgrammeDetailsMixin(MultiTableMixin):
    hierarchy_type = -1
    table_pagination = False

    def programme_code(self):
        return ProgrammeCode.objects.get(
            pk=self.kwargs['programme_code'],
        )

    def forecast_expenditure_type(self):
        return self.kwargs['forecast_expenditure_type']

    def programme_code_form(self):
        return ProgrammeForm()

    def get_tables(self):
        """
         Return an array of table instances containing data.
        """
        forecast_expenditure_type_id = self.kwargs['forecast_expenditure_type']
        programme_code_id = self.kwargs['programme_code']
        pivot_filter = {
            PROGRAMME_CODE: f"{programme_code_id}",
            FORECAST_EXPENDITURE_TYPE_ID: f"{forecast_expenditure_type_id}",
        }
        arg_name = filter_codes[self.hierarchy_type]
        if arg_name:
            filter_code = self.kwargs[arg_name]
            pivot_filter[filter_selectors[self.hierarchy_type]] = f"{filter_code}"

        nac_data = MonthlyFigureAmount.pivot.subtotal_data(
            programme_details_display_sub_total_column,
            programme_details_sub_total,
            nac_columns.keys(),
            pivot_filter,
            order_list=programme_details_order_list,
            show_grand_total=False
        )

        nac_table = ForecastSubTotalTable(nac_columns, nac_data)
        nac_table.attrs['caption'] = "Expenditure Report"

        self.tables = [
            nac_table,
        ]
        return self.tables


class DITProgrammeDetailsView(
    ForecastViewPermissionMixin,
    ForecastProgrammeDetailsMixin,
    TemplateView,
):
    template_name = "forecast/view/programme_details/dit.html"
    hierarchy_type = SHOW_DIT

    def post(self, request, *args, **kwargs):
        programme_code_id = request.POST.get(
            'programme_code',
            None,
        )

        if programme_code_id:
            return HttpResponseRedirect(
                reverse(
                    "programme_details_dit",
                    kwargs={'programme_code': programme_code_id,
                            'forecast_expenditure_type': self.forecast_expenditure_type(),
                            }

                )
            )
        else:
            raise Http404("Budget Type not found")


class GroupProgrammeDetailsView(
    ForecastViewPermissionMixin,
    ForecastProgrammeDetailsMixin,
    TemplateView,
):
    pass
#     template_name = "forecast/view/programme_details/group.html"
#     hierarchy_type = SHOW_GROUP
#
#     def group(self):
#         return DepartmentalGroup.objects.get(
#             group_code=self.kwargs['group_code'],
#             active=True,
#         )
#
#     def post(self, request, *args, **kwargs):
#         programme_code_id = request.POST.get(
#             'programme_code',
#             None,
#         )
#
#         if programme_code_id:
#             return HttpResponseRedirect(
#                 reverse(
#                     "programme_details_group",
#                     kwargs={'group_code': self.group().group_code,
#                             'programme_code': programme_code_id,
#                             'forecast_expenditure_type': self.forecast_expenditure_type(),
#                             }
#                 )
#             )
#         else:
#             raise Http404("Budget Type not found")


class DirectorateProgrammeDetailsView(
    ForecastViewPermissionMixin,
    ForecastProgrammeDetailsMixin,
    TemplateView,
):
    pass
#     template_name = "forecast/view/programme_details/directorate.html"
#     hierarchy_type = SHOW_DIRECTORATE
#
#     def directorate(self):
#         return Directorate.objects.get(
#             directorate_code=self.kwargs['directorate_code'],
#             active=True,
#         )
#
#     def post(self, request, *args, **kwargs):
#         programme_code_id = request.POST.get(
#             'programme_code',
#             None,
#         )
#
#         if programme_code_id:
#             return HttpResponseRedirect(
#                 reverse(
#                     "programme_details_directorate",
#                     kwargs={'directorate_code': self.directorate().directorate_code,
#                             'programme_code': programme_code_id,
#                             'forecast_expenditure_type': self.forecast_expenditure_type(),
#                             }
#                 )
#             )
#         else:
#             raise Http404("Budget Type not found")
#

