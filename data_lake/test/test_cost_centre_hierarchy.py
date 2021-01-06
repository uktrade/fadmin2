from rest_framework.reverse import reverse

from data_lake.test.utils import DataLakeTesting

from costcentre.test.factories import (
    ArchivedCostCentreFactory,
    CostCentreFactory,
)


class HierarchyTests(DataLakeTesting):
    def test_hierarchy_data_returned_in_response(self):
        self.current_code = CostCentreFactory.create().cost_centre_code
        self.archived_code = ArchivedCostCentreFactory.create(
            financial_year_id=2019
        ).cost_centre_code

        self.test_url = "http://testserver" + reverse("data_lake_hierachy")
        self.row_lenght = 11
        self.code_position = 4
        self.check_data()
