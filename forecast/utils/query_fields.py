# monthly_figure__financial_code__programme__budget_type_fk__budget_type_display
# indicates if DEL, AME, ADMIN
# It is used in every view
BUDGET_TYPE =  "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display"  # noqa

BUDGET_TYPE_ORDER =  "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display_order"  # noqa

EXPENDITURE_CATEGORY_ID = "monthly_figure__financial_code__natural_account_code__expenditure_category__id"  # noqa

PROGRAMME_CODE = "monthly_figure__financial_code__programme__programme_code"
PROGRAMME_DESCRIPTION = "monthly_figure__financial_code__programme__programme_description"

FORECAST_EXPENDITURE_TYPE_ID = "monthly_figure__financial_code__forecast_expenditure_type__id"  # noqa

COST_CENTRE_NAME = "monthly_figure__financial_code__cost_centre__cost_centre_name"
COST_CENTRE_CODE = "monthly_figure__financial_code__cost_centre__cost_centre_code"

DIRECTORATE_NAME = "monthly_figure__financial_code__cost_centre__directorate__directorate_name"  # noqa
DIRECTORATE_CODE = "monthly_figure__financial_code__cost_centre__directorate__directorate_code"  # noqa

GROUP_NAME = "monthly_figure__financial_code__cost_centre__directorate__group__group_name"  # noqa
GROUP_CODE = "monthly_figure__financial_code__cost_centre__directorate__group__group_code"  # noqa

NAC_CODE = "monthly_figure__financial_code__natural_account_code__natural_account_code"
NAC_NAME = "monthly_figure__financial_code__natural_account_code__natural_account_code_description"  # noqa

PROJECT_CODE = "monthly_figure__financial_code__project_code__project_code"
PROJECT_NAME = "monthly_figure__financial_code__project_code__project_description"


SHOW_DIT = 0
SHOW_GROUP = 1
SHOW_DIRECTORATE = 2
SHOW_COSTCENTRE = 3


cost_centre_columns = {
    BUDGET_TYPE: "Budget Type",
    COST_CENTRE_NAME: "Cost Centre Description",
    COST_CENTRE_CODE: "Cost Centre Code",
}

directorate_columns = {
    BUDGET_TYPE: "Budget Type",
    DIRECTORATE_NAME: "Directorate Description",
    DIRECTORATE_CODE: "Directorate Code",
}

group_columns = {
    BUDGET_TYPE: "Budget Type",
    GROUP_NAME: "Departmental Group Code",
    GROUP_CODE: "Departmental Group Description",
}
hierarchy_order_list = [BUDGET_TYPE_ORDER]
hierarchy_sub_total = [BUDGET_TYPE]

# programme data
programme_columns = {
    BUDGET_TYPE: "Hidden",
    FORECAST_EXPENDITURE_TYPE_ID: "Hidden",
    "monthly_figure__financial_code__forecast_expenditure_type__forecast_expenditure_type_description": "Hidden1",  # noqa
    "monthly_figure__financial_code__forecast_expenditure_type__forecast_expenditure_type_name": "Expenditure Type",  # noqa
    PROGRAMME_DESCRIPTION: "Programme Description",
    PROGRAMME_CODE: "Programme Code",
}
programme_order_list = [
    BUDGET_TYPE_ORDER,
    "monthly_figure__financial_code__forecast_expenditure_type__forecast_expenditure_type_display_order",  # noqa
]
programme_sub_total = [
    BUDGET_TYPE,
    "monthly_figure__financial_code__forecast_expenditure_type__forecast_expenditure_type_description",  # noqa
]
programme_display_sub_total_column = PROGRAMME_DESCRIPTION

# Expenditure data
expenditure_columns = {
    BUDGET_TYPE: "Hidden",
    EXPENDITURE_CATEGORY_ID: "Hidden",
    "monthly_figure__financial_code__natural_account_code__expenditure_category__NAC_category__NAC_category_description": "Budget Grouping",  # noqa
    "monthly_figure__financial_code__natural_account_code__expenditure_category__grouping_description":"Budget Category",  # noqa
}
expenditure_sub_total = [
    BUDGET_TYPE,
    "monthly_figure__financial_code__natural_account_code__expenditure_category__NAC_category__NAC_category_description",  # noqa
]
expenditure_display_sub_total_column = (
    "monthly_figure__financial_code__natural_account_code__expenditure_category__grouping_description"  # noqa
)
expenditure_order_list = [
    BUDGET_TYPE_ORDER,  # noqa
    "monthly_figure__financial_code__natural_account_code__expenditure_category__NAC_category__NAC_category_description",  # noqa
]

# Project data
project_columns = {
    BUDGET_TYPE: 'Budget Type',
    PROJECT_NAME: "Project Description",
    PROJECT_CODE: "Project Code",
}
project_order_list = [
    BUDGET_TYPE_ORDER,
]
project_sub_total = [
    BUDGET_TYPE,
]
project_display_sub_total_column = PROJECT_NAME

filter_codes = ['', 'group_code', 'directorate_code', 'cost_centre_code']
filter_selectors = [
    '',
    GROUP_CODE,
    DIRECTORATE_CODE,
    COST_CENTRE_CODE,
]

hierarchy_columns = [
    group_columns,
    directorate_columns,
    cost_centre_columns,
    cost_centre_columns,
]

hierarchy_sub_total_column = [
    GROUP_NAME,
    DIRECTORATE_NAME,
    COST_CENTRE_NAME,
    COST_CENTRE_NAME,
]

expenditure_view = [
    'expenditure_details_dit',
    'expenditure_details_group',
    'expenditure_details_directorate',
    'expenditure_details_cost_centre',
]
# NAC data
nac_columns = {
    "monthly_figure__financial_code__natural_account_code__expenditure_category__grouping_description": "Hidden",  # noqa
    NAC_NAME: "Natural Account Code Description",
    NAC_CODE: "Code",  # noqa
}
nac_sub_total = [
    "monthly_figure__financial_code__natural_account_code__expenditure_category__grouping_description",  # noqa
]
nac_display_sub_total_column = NAC_NAME

nac_order_list = [
    NAC_NAME,
]

# BUDGET_TYPE: "monthly_figure__financial_code__programme__budget_type_fk__budget_type_display",
# "monthly_figure__financial_code__forecast_expenditure_type__id": "Hidden1",  # noqa
# "monthly_figure__financial_code__programme__programme_code": "Programme Code",

# programme details data
programme_details_dit_columns = {
    "monthly_figure__financial_code__natural_account_code__expenditure_category__grouping_description": "Hidden",  # noqa
    GROUP_NAME: "Departmental Group Code",
    GROUP_CODE: "Departmental Group Description",
}
programme_details_group_columns = {
    "monthly_figure__financial_code__natural_account_code__expenditure_category__grouping_description": "Hidden",  # noqa
    DIRECTORATE_NAME: "Directorate Description",
    DIRECTORATE_CODE: "Directorate Code",
}
programme_details_directorate_columns = {
    "monthly_figure__financial_code__natural_account_code__expenditure_category__grouping_description": "Hidden",  # noqa
    COST_CENTRE_NAME: "Cost Centre Description",
    COST_CENTRE_CODE: "Cost Centre Code",
}
programme_details_sub_total = [
    "monthly_figure__financial_code__natural_account_code__expenditure_category__grouping_description",  # noqa
]
programme_details_display_sub_total_column = (
    NAC_NAME,
)
programme_details_order_list = [
    NAC_NAME,
]

programme_details_hierarchy_columns = [
    programme_details_dit_columns,
    programme_details_group_columns,
    programme_details_directorate_columns,
    '',
]

programme_details_hierarchy_sub_total_column = [
    GROUP_NAME,
    DIRECTORATE_NAME,
    COST_CENTRE_NAME,
    '',]


