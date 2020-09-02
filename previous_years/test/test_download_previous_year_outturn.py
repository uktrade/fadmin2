import io

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from openpyxl import load_workbook

from chartofaccountDIT.test.factories import (
    HistoricalAnalysis1Factory,
    HistoricalAnalysis2Factory,
    HistoricalNaturalCodeFactory,
    HistoricalProgrammeCodeFactory,
    HistoricalProjectCodeFactory,
)

from core.models import FinancialYear
from core.test.test_base import RequestFactoryBase

from costcentre.test.factories import ArchivedCostCentreFactory

from forecast.views.view_forecast.export_forecast_data import (
    export_forecast_data_cost_centre,
    export_forecast_data_directorate,
    export_forecast_data_dit,
    export_forecast_data_group,
)

from previous_years.models import (
    ArchivedFinancialCode,
    ArchivedForecastData,
)


class DownloadPastYearForecastHierarchyTest(TestCase, RequestFactoryBase):

    #     self.budget = create_budget(financial_code_obj, year_obj)
    #     self.year_total = self.amount_apr + self.amount_may
    #     self.underspend_total = self.budget - self.amount_apr - self.amount_may
    #     self.spend_to_date_total = self.amount_apr

    def setUp(self):
        RequestFactoryBase.__init__(self)
        # 2019 is created when the database is created, so it exists
        self.archived_year = 2019
        archived_year_obj = FinancialYear.objects.get(pk=self.archived_year)
        self.cost_centre_code = "109189"
        self.group_code = "1090TT"
        self.directorate_code = "10900T"
        self.natural_account_code = 52191003
        self.programme_code = "310940"
        self.project_code = "0123"
        self.analisys1 = "00798"
        self.analisys2 = "00321"
        cc_obj = ArchivedCostCentreFactory.create(
            cost_centre_code=self.cost_centre_code,
            directorate_code=self.directorate_code,
            group_code=self.group_code,
            financial_year=archived_year_obj,
        )
        project_obj = HistoricalProjectCodeFactory.create(
            project_code=self.project_code, financial_year=archived_year_obj
        )
        programme_obj = HistoricalProgrammeCodeFactory.create(
            programme_code=self.programme_code, financial_year=archived_year_obj
        )
        nac_obj = HistoricalNaturalCodeFactory.create(
            natural_account_code=self.natural_account_code,
            economic_budget_code="CAPITAL",
            financial_year=archived_year_obj,
        )
        analysis2_obj = HistoricalAnalysis2Factory.create(
            analysis2_code=self.analisys2, financial_year=archived_year_obj
        )
        analysis1_obj = HistoricalAnalysis1Factory.create(
            analysis1_code=self.analisys1, financial_year=archived_year_obj
        )
        financial_code_obj = ArchivedFinancialCode.objects.create(
            programme=programme_obj,
            cost_centre=cc_obj,
            natural_account_code=nac_obj,
            analysis1_code=analysis1_obj,
            analysis2_code=analysis2_obj,
            project_code=project_obj,
            financial_year=archived_year_obj,
        )

        previous_year_obj = ArchivedForecastData.objects.create(
            financial_year=archived_year_obj, financial_code=financial_code_obj,
        )
        self.outturn = {
            "budget": 1234500,
            "apr": 1200000,
            "may": 3412000,
            "jun": 9876000,
            "jul": 5468970,
            "aug": 3421900,
            "sep": 6901110,
            "oct": 7622200,
            "nov": 6955501,
            "dec": 8434422,
            "jan": 5264091,
            "feb": 4521111,
            "mar": 9090111,
            "adj01": 5464644,
            "adj02": 2118976,
            "adj03": 3135450,
        }
        previous_year_obj.budget = self.outturn["budget"] * 100
        previous_year_obj.apr = self.outturn["apr"] * 100
        previous_year_obj.may = self.outturn["may"] * 100
        previous_year_obj.jun = self.outturn["jun"] * 100
        previous_year_obj.jul = self.outturn["jul"] * 100
        previous_year_obj.aug = self.outturn["aug"] * 100
        previous_year_obj.sep = self.outturn["sep"] * 100
        previous_year_obj.oct = self.outturn["oct"] * 100
        previous_year_obj.nov = self.outturn["nov"] * 100
        previous_year_obj.dec = self.outturn["dec"] * 100
        previous_year_obj.jan = self.outturn["jan"] * 100
        previous_year_obj.feb = self.outturn["feb"] * 100
        previous_year_obj.mar = self.outturn["mar"] * 100
        previous_year_obj.adj1 = self.outturn["adj01"] * 100
        previous_year_obj.adj2 = self.outturn["adj02"] * 100
        previous_year_obj.adj3 = self.outturn["adj03"] * 100
        previous_year_obj.save()
        # Assign forecast view permission
        can_view_forecasts = Permission.objects.get(codename="can_view_forecasts")
        self.test_user.user_permissions.add(can_view_forecasts)
        self.test_user.save()

    def test_dit_download(self):
        dit_url = self.factory_get(
            reverse("export_forecast_data_dit", kwargs={"period": self.archived_year}),
            export_forecast_data_dit,
            period=self.archived_year,
        )

        self.assertEqual(dit_url.status_code, 200)
        file = io.BytesIO(dit_url.content)
        wb = load_workbook(filename=file)
        ws = wb.active
        # Check group
        assert ws["A1"].value == "Group name"
        assert ws["B2"].value == self.group_code

    def test_group_download(self):
        response = self.factory_get(
            reverse(
                "export_forecast_data_group",
                kwargs={"group_code": self.group_code, "period": self.archived_year, },
            ),
            export_forecast_data_group,
            group_code=self.group_code,
            period=self.archived_year,
        )

        self.assertEqual(response.status_code, 200)

        file = io.BytesIO(response.content)
        wb = load_workbook(filename=file)
        ws = wb.active
        # Check group
        assert ws["A1"].value == "Group name"
        assert ws["B2"].value == self.group_code

    def test_directorate_download(self):
        response = self.factory_get(
            reverse(
                "export_forecast_data_directorate",
                kwargs={
                    "directorate_code": self.directorate_code,
                    "period": self.archived_year,
                },
            ),
            export_forecast_data_directorate,
            directorate_code=self.directorate_code,
            period=self.archived_year,
        )

        self.assertEqual(response.status_code, 200)

        file = io.BytesIO(response.content)
        wb = load_workbook(filename=file, read_only=True)
        ws = wb.active
        # Check group
        assert ws["A1"].value == "Group name"
        assert ws["B2"].value == self.group_code

    def test_cost_centre_download(self):
        response = self.factory_get(
            reverse(
                "export_forecast_data_cost_centre",
                kwargs={
                    "cost_centre": self.cost_centre_code,
                    "period": self.archived_year,
                },
            ),
            export_forecast_data_cost_centre,
            cost_centre=self.cost_centre_code,
            period=self.archived_year,
        )

        self.assertEqual(response.status_code, 200)

        file = io.BytesIO(response.content)
        wb = load_workbook(filename=file)
        ws = wb.active
        # Check group
        assert ws["A1"].value == "Group name"
        assert ws["B2"].value == self.group_code
