from guardian.shortcuts import (
    assign_perm as guardian_assign_perm,
    get_objects_for_user as guardian_get_objects_for_user,
)

from django.contrib.auth import get_user_model
from django.test import TestCase

from costcentre.test.factories import (
    CostCentreFactory,
)

from forecast.models import ForecastPermission
from forecast.permission_shortcuts import (
    assign_perm,
    get_objects_for_user,
    NoForecastViewPermission,
)
from forecast.test.factories import ForecastPermissionFactory
from forecast.views.edit_forecast import (
    TEST_COST_CENTRE,
)


class PermissionShortcutsTest(
    TestCase,
):
    def setUp(self):
        self.test_user, _ = get_user_model().objects.get_or_create(
            email="test@test.com"
        )
        self.cost_centre = CostCentreFactory.create(
            cost_centre_code=TEST_COST_CENTRE
        )

    def test_assign_perm(self):
        assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre,
        )
        # check that forecast permission assigned
        forecast_permission = ForecastPermission.objects.filter(
            user=self.test_user,
        ).first()

        assert forecast_permission is not None
        # check guardian permissions created

        cost_centres = guardian_get_objects_for_user(
            self.test_user,
            "costcentre.change_costcentre",
        )

        assert len(cost_centres) == 1

    def test_get_objects_for_user(self):
        with self.assertRaises(NoForecastViewPermission):
            get_objects_for_user(
                self.test_user,
                "costcentre.change_costcentre",
            )

        ForecastPermissionFactory(
            user=self.test_user,
        )

        guardian_assign_perm(
            "change_costcentre",
            self.test_user,
            self.cost_centre,
        )

        cost_centres = get_objects_for_user(
            self.test_user,
            "costcentre.change_costcentre",
        )

        assert len(cost_centres) == 1
