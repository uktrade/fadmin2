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

from gifthospitality.models import GiftAndHospitality, GiftAndHospitalityClassification, GiftAndHospitalityCompany, GiftAndHospitalityCategory, Grade

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

        classification = GiftAndHospitalityClassification(sequence_no=10, gif_hospitality_classification="Test Classification")
        classification.save()

        category = GiftAndHospitalityCategory(sequence_no=10, gif_hospitality_category="Test Category")
        category.save()

        # action_taken = GiftAndHospitality(action_taken="Rejected")
        # action_taken.save()

    def test_gift_hospitality_receive_form(self):
        response = reverse("gifthospitality:gift-received",)

        response = self.client.get(response)

        self.assertEqual(response.status_code, 200)

        classification_filter = GiftAndHospitalityClassification.objects.get(sequence_no=10)
        # print(classification_filter)

        category_filter = GiftAndHospitalityCategory.objects.get(sequence_no=10)

        grade_filter = Grade.objects.all()

        print(grade_filter)


        gift_hospitality_received_data = {
            'classification': classification_filter,     # Required
            'category': category_filter,       # Required
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
