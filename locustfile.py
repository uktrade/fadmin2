import os

from locust import (
    HttpLocust,
    TaskSet,
    task,
    between,
)


sso_headers = {
    "Cookie": f"csrftoken={os.environ['CRSF_TOKEN']}; sessionid={os.environ['SESSION_ID']}"
}


class UserBehaviour(TaskSet):
    @task(1)
    def index(self):
        self.client.get("", headers=sso_headers)

    @task(2)
    def post_to_edit_forecast(self):
        self.client.post(
            f"/forecast/edit/{os.environ['TEST_COST_CENTRE_CODE']}/",
            data={
                "all_selected": True,
                "paste_content": """Programme code	Programme code Description	Natural Account code	Natural Account Code Description	Contract Code	Market Code	Project Code	Budget	Apr	May	Jun	Jul	Aug	Sep	Oct	Nov	Dec	Jan	Feb	Mar	Forecast outturn	Variance -overspend/underspend	Year to Date Actuals	Group name	Group code	Directorate name	Directorate code	Cost Centre name	Cost Centre code	Budget Grouping	Expenditure type	Expenditure type description	Budget type	Budget Category	Budget/Forecast NAC	Budget/Forecast NAC Description	NAC Expenditure Type	Contract Description	Market Description	Project Description
300028	NOT IN USE - Invest in Great Britain	11272001	Additions - Cost - Leasehold Improvements	00001			0.00	0.00	0.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	990.00	-990.00	0.00	Centrally Managed Resources	1090TT	Prosperity Contingency	10901A	Locust	123456	Capital	Capital	Capital	DEL	Estates (Capital)	11612001	Additions  - Cost - Furniture & Fittings	CAPITAL	Provision of Event Management Services -  Specialist Live Events Lots 2- 7		
300047	NOT IN USE - Non Capital Equipment	11272002	Clearing Account - Cost - Leasehold Improvements	00002			0.00	0.00	0.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	990.00	-990.00	0.00	Centrally Managed Resources	1090TT	Prosperity Contingency	10901A	Locust	123456	Capital	Capital	Capital	DEL	Estates (Capital)	11612001	Additions  - Cost - Furniture & Fittings	CAPITAL	Provision of Full Creative Services		
300056	NOT IN USE - ECJU	11412001	Additions  - Cost - Computer Equipment	00003			0.00	0.00	0.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	990.00	-990.00	0.00	Centrally Managed Resources	1090TT	Prosperity Contingency	10901A	Locust	123456	Capital	Capital	Capital	DEL	Digital & ICT (Capital)	14112001	Additions  - Cost - Information Technology	CAPITAL	Provision of Event Management Services. Lot 1 - Specialist Services		
300058	NOT IN USE - ECJU Training and Awareness programme income and expenditure	11412002	Clearing Account   - Cost - Computer Equipment	00004			0.00	0.00	0.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	99.00	990.00	-990.00	0.00	Centrally Managed Resources	1090TT	Prosperity Contingency	10901A	Locust	123456	Capital	Capital	Capital	DEL	Digital & ICT (Capital)	14112001	Additions  - Cost - Information Technology	CAPITAL	Media Planning and Buying - International		
						Grand Total:	0	0	0	396	396	396	396	396	396	396	396	396	396	3960	-3960	0																""",
                "csrfmiddlewaretoken": os.environ['CRSF_TOKEN'],
                "headers": sso_headers,
            },
        )


class FFTUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(5, 9)
