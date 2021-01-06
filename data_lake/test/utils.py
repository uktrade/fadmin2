import csv

import io

from data_lake.test.test_hawk import hawk_auth_sender

from rest_framework.test import APIClient


def return_csv_as_list(test_url):
    sender = hawk_auth_sender(url=test_url)
    response = APIClient().get(
        test_url,
        content_type="",
        HTTP_AUTHORIZATION=sender.request_header,
        HTTP_X_FORWARDED_FOR="1.2.3.4, 123.123.123.123",
    )

    assert response["Content-Type"] == "text/csv"
    content = response.content.decode('utf-8')
    data = csv.reader(io.StringIO(content))
    return list(data)

