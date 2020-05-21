from datetime import datetime

from bs4 import BeautifulSoup

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import (
    TestCase,
)
from django.urls import reverse, path

from core.test.test_base import RequestFactoryBase

from gifthospitality.models import GiftAndHospitality, GiftAndHospitalityClassification

from gifthospitality.forms import GiftAndHospitalityReceivedForm
from gifthospitality.views import GiftHospitalityReceivedView

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class GiftHospitalityReceivedFormTest(TestCase, RequestFactoryBase):
    def setUp(self):
        RequestFactoryBase.__init__(self)

        self.client.login(
            username=self.test_user_email,
            password=self.test_password,
        )

    def test_gift_hospitality_receive_form(self):
        response = reverse("gifthospitality:gift-received",)

        response = self.client.get(response)

        self.assertEqual(response.status_code, 200)

        classification_filter = GiftAndHospitalityClassification.objects.get()
        print(classification_filter)

        gift_hospitality_received_data = {
            'classification': '88',     # Required
            'category': 'Meeting company to discuss Trade and/or Investment opportunities',       # Required
                                          'date_offered': '22-03-2005',     # Required
                                          'action_taken': 'Rejected', # Required
                                          'venue': 'Normal Venue',  # Required
                                          'reason': 'Recommended by FD',  # Required
                                          'value': '12',  # Required
                            'rep': 'Someone from DIT',  # Required
                            'grade': 'EO',  # Required
                            'group': 'Departmental Group 0',  # Required
                            'company_rep': 'Someone from a company',  # Required
                            'company': 'ADS',  # Required
                                                            }


        self.assertContains(response, "govuk-button")
        soup = BeautifulSoup(response.content, features="html.parser")

        save_button = soup.find("save", class_="govuk-button")

        gift_hospitality_received_form = GiftAndHospitalityReceivedForm(data=gift_hospitality_received_data)
        # print (gift_hospitality_received_form)

        # self.assertTrue(gift_hospitality_received_form.is_valid())

        # redirect = save_button.click()
        #
        # self.assertEqual(redirect.status_code, 302)
