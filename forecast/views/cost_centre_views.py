from django.urls import reverse
from django.views.generic.base import TemplateView

from guardian.shortcuts import get_objects_for_user

from costcentre.forms import (
    AllCostCentresForm,
    CostCentreViewModeForm,
    MyCostCentresForm,
)


class ChooseCostCentreView(TemplateView):
    template_name = "forecast/choose_cost_centre.html"

    def cost_centre_mode_form(self):
        return CostCentreViewModeForm()

    def all_cost_centres_form(self):
        return AllCostCentresForm()

    def my_cost_centres_form(self):
        return MyCostCentresForm(
            user=self.request.user,
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        cost_centre_code = request.POST.get(
            'cost_centre',
            None,
        )
        if cost_centre_code:
            return reverse(
                "edit_forecast",
                kwargs={'cost_centre_code': cost_centre_code}
            )

        return self.render_to_response(context)
