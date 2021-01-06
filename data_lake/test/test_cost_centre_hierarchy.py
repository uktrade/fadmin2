from rest_framework.reverse import reverse

from data_lake.test.test_hawk import hawk_auth_sender

from django.test import (
    TestCase,
    override_settings,
)

from rest_framework.test import APIClient

from costcentre.test.factories import (
    ArchivedCostCentreFactory,
    CostCentreFactory,
)


class HierarchyTests(TestCase):
    @override_settings(
        HAWK_INCOMING_ACCESS_KEY="some-id", HAWK_INCOMING_SECRET_KEY="some-secret",
    )
    def test_hierarchy_data_returned_in_response(self):
        cost_centre = CostCentreFactory.create().cost_centre_code
        archived_cost_centre = ArchivedCostCentreFactory.create(
            financial_year_id=2019
        ).cost_centre_code

        test_url = "http://testserver" + reverse("data_lake_hierachy")
        sender = hawk_auth_sender(url=test_url)
        response = APIClient().get(
            test_url,
            content_type="",
            HTTP_AUTHORIZATION=sender.request_header,
            HTTP_X_FORWARDED_FOR="1.2.3.4, 123.123.123.123",
        )

        assert response["Content-Type"] == "text/csv"

        rows = response.content.decode("utf-8").split("\n")

        cols = rows[0].split(",")
        assert len(cols) == 11

        cols = rows[1].split(",")
        assert str(cols[4]) == str(cost_centre)

        # # Check the archived value
        assert str(cols[4]) == str(archived_cost_centre)
