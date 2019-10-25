from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from costcentre.models import CostCentre


class NoCostCentreCodeInURLError(Exception):
    pass


class ForecastBaseView(UserPassesTestMixin, TemplateView):
    cost_centre_code = None

    def test_func(self):
        if 'cost_centre_code' not in self.kwargs:
            raise NoCostCentreCodeInURLError(
                "No cost centre code provided in URL"
            )

        self.cost_centre_code = self.kwargs["cost_centre_code"]

        cost_centre = CostCentre.objects.get(
            cost_centre_code=self.kwargs["cost_centre_code"]
        )

        return self.request.user.has_perm(
            "view_costcentre", cost_centre
        ) and self.request.user.has_perm(
            "change_costcentre",
            cost_centre
        )

    def handle_no_permission(self):
        return redirect("costcentre")