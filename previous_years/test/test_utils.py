from django.contrib.auth.models import Permission
from django.test import TestCase

from chartofaccountDIT.test.factories import (
    HistoricalAnalysis1Factory,
    HistoricalAnalysis2Factory,
    HistoricalExpenditureCategoryFactory,
    HistoricalNaturalCodeFactory,
    HistoricalProgrammeCodeFactory,
    HistoricalProjectCodeFactory,
)

from core.models import FinancialYear
from core.test.test_base import RequestFactoryBase

from costcentre.test.factories import ArchivedCostCentreFactory

from previous_years.models import (
    ArchivedFinancialCode,
    ArchivedForecastData,
)


class DownloadPastYearForecastSetup(TestCase, RequestFactoryBase):

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
        self.budget_type_id = "AME"
        programme_obj = HistoricalProgrammeCodeFactory.create(
            programme_code=self.programme_code,
            budget_type_id=self.budget_type_id,
            financial_year=archived_year_obj
        )

        expenditure_category_obj = HistoricalExpenditureCategoryFactory.create(
            financial_year=archived_year_obj
        )
        self.expenditure_category_id = expenditure_category_obj.id
        nac_obj = HistoricalNaturalCodeFactory.create(
            natural_account_code=self.natural_account_code,
            economic_budget_code="CAPITAL",
            expenditure_category=expenditure_category_obj,
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
        # __forecast_expenditure_type_name"
        self.expenditure_type_name = financial_code_obj.forecast_expenditure_type
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
