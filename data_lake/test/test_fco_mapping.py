from data_lake.test.utils import DataLakeTesting

from chartofaccountDIT.test.factories import (
    FCOMappingFactory,
    HistoricalFCOMappingFactory,
)


class FCOMappingFactoryTests(DataLakeTesting):
    def test_data_returned_in_response(self):
        self.current_code = FCOMappingFactory.create().fco_code
        self.archived_code = HistoricalFCOMappingFactory.create(
            financial_year_id=2019
        ).fco_code

        self.url_name = "data_lake_expenditure_category"
        self.row_lenght = 7
        self.code_position = 6
        self.check_data()
