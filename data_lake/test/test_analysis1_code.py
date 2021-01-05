from rest_framework.reverse import reverse

from data_lake.test.test_hawk import hawk_auth_sender

from django.test import (
    TestCase,
    override_settings,
)

from rest_framework.test import APIClient

from chartofaccountDIT.test.factories import (
    HistoricalAnalysis1Factory,
    Analysis1Factory,
)


class Analysis1CodeTests(TestCase):
    @override_settings(
        HAWK_INCOMING_ACCESS_KEY="some-id", HAWK_INCOMING_SECRET_KEY="some-secret",
    )
    def test_data_returned_in_response(self):
        analysis1_code = Analysis1Factory.create().analysis1_code
        archived_analysis1_code = \
            HistoricalAnalysis1Factory.create().analysis1_code

        test_url = "http://testserver" + reverse("data_lake_analysis1_code")
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
        assert len(cols) == 5

        cols = rows[1].split(",")
        assert str(cols[0]) == str(analysis1_code)
        # Check the archived value
        cols = rows[2].split(",")
        assert str(cols[0]) == str(archived_analysis1_code)
