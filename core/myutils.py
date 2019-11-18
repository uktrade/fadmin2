# Collection of useful functions and classes
import datetime

from django.conf import settings

import requests

from .models import FinancialYear


def get_current_financial_year():
    y = FinancialYear.objects.filter(current=True)
    if y:
        current_financial_year = y.last().financial_year
    else:
        # If there is a data problem
        # and the current year is not
        # defined, return the financial
        # year for the current date
        # The UK financial year starts
        # in April, so Jan, Feb and Mar
        # are part of the previous year
        today = datetime.datetime.now()
        current_month = today.month
        current_financial_year = today.year
        if current_month < 3 or (current_month == 4 and today.day < 5):
            # before 5th April, the financial
            # year it is one year behind the
            # calendar year
            current_financial_year -= (
                1
            )

    return current_financial_year


class GetValidYear:
    regex = '2018|2019'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value


def run_anti_virus(file):
    # Check file with AV web service
    if settings.IGNORE_ANTI_VIRUS:
        return {'malware': False}

    files = {"file": file}
    auth = (
        settings.CLAM_AV_USERNAME,
        settings.CLAM_AV_PASSWORD,
    )
    response = requests.post(
        settings.CLAM_AV_URL,
        auth=auth,
        files=files,
    )

    return response.json()
