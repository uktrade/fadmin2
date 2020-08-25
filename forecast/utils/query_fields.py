financial_code_prefix = "financial_code__"
SHOW_DIT = 0
SHOW_GROUP = 1
SHOW_DIRECTORATE = 2
SHOW_COSTCENTRE = 3


class ViewForecastFields():
    def __init__(self, period=0):
        self.current = period < 2000

    financial_code_prefix = "financial_code__"
    # indicates if DEL, AME, ADMIN
    budget_type_field = f"{financial_code_prefix}programme__budget_type__budget_type_display"
    budget_type_order_field = f"{financial_code_prefix}programme__budget_type__budget_type_display_order"  # noqa
    budget_type_edit_order_field = f"{financial_code_prefix}programme__budget_type__budget_type_edit_display_order"  # noqa

    # Categories defined by DIT: i.e. Consultancy, Contingency, Contractors, etc
    budget_category_id_field = f"{financial_code_prefix}natural_account_code__expenditure_category__id"  # noqa
    budget_category_name_field = f"{financial_code_prefix}natural_account_code__expenditure_category__grouping_description"   # noqa

    # PAY, NON-PAY, CAPITAL, NON-CASH
    budget_grouping_field = f"{financial_code_prefix}natural_account_code__expenditure_category__NAC_category__NAC_category_description"   # noqa
    budget_grouping_order_field = f"{financial_code_prefix}natural_account_code__expenditure_category__NAC_category__NAC_category_display_order"   # noqa
    budget_nac_field = f"{financial_code_prefix}natural_account_code__expenditure_category__linked_budget_code"  # noqa
    budget_nac_description_field = f"{financial_code_prefix}natural_account_code__expenditure_category__linked_budget_code__natural_account_code_description"  # noqa

    # Admin, Capital or Programme
    expenditure_type_name_field = f"{financial_code_prefix}forecast_expenditure_type__forecast_expenditure_type_name"  # noqa
    expenditure_type_description_field = f"{financial_code_prefix}forecast_expenditure_type__forecast_expenditure_type_description"  # noqa
    expenditure_type_order_field = f"{financial_code_prefix}forecast_expenditure_type__forecast_expenditure_type_display_order"   # noqa

    programme_code_field = f"{financial_code_prefix}programme__programme_code"
    programme_name_field = f"{financial_code_prefix}programme__programme_description"

    cost_centre_name_field = f"{financial_code_prefix}cost_centre__cost_centre_name"
    cost_centre_code_field = f"{financial_code_prefix}cost_centre__cost_centre_code"

    directorate_name_field = f"{financial_code_prefix}cost_centre__directorate__directorate_name"
    directorate_code_field = f"{financial_code_prefix}cost_centre__directorate__directorate_code"

    group_name_field = f"{financial_code_prefix}cost_centre__directorate__group__group_name"
    group_code_field = f"{financial_code_prefix}cost_centre__directorate__group__group_code"

    nac_code_field = f"{financial_code_prefix}natural_account_code__natural_account_code"
    nac_name_field = f"{financial_code_prefix}natural_account_code__natural_account_code_description"  # noqa
    nac_expenditure_type_field = f"{financial_code_prefix}natural_account_code__economic_budget_code"  # noqa


    project_code_field = f"{financial_code_prefix}project_code__project_code"
    project_name_field = f"{financial_code_prefix}project_code__project_description"

    analysis1_code_field = f"{financial_code_prefix}analysis1_code__analysis1_code"
    analysis1_name_field = f"{financial_code_prefix}analysis1_code__analysis1_description"

    analysis2_code_field = f"{financial_code_prefix}analysis2_code__analysis2_code"
    analysis2_name_field = f"{financial_code_prefix}analysis2_code__analysis2_description"

    cost_centre_columns = {
        budget_type_field: "Budget type",
        cost_centre_name_field: "Cost Centre description",
        cost_centre_code_field: "code",
    }

    directorate_columns = {
        budget_type_field: "Budget Type",
        directorate_name_field: "Directorate description",
        directorate_code_field: "code",
    }

    group_columns = {
        budget_type_field: "Budget Type",
        group_name_field: "Departmental Group description",
        group_code_field: "code",
    }

    hierarchy_sub_total = [budget_type_field]

    # programme data
    programme_columns = {
        budget_type_field: "Hidden",
        expenditure_type_description_field: "Hidden",
        expenditure_type_name_field: "Expenditure type",
        programme_name_field: "Programme code",
        programme_code_field: "code",
    }

    programme_order_list = [
        budget_type_order_field,
        expenditure_type_order_field,
    ]
    programme_sub_total = [
        budget_type_field,
        expenditure_type_description_field,
    ]
    programme_display_sub_total_column = programme_name_field

    programme_detail_view = [
        'programme_details_dit',
        'programme_details_group',
        'programme_details_directorate',
    ]

    # Expenditure data
    expenditure_columns = {
        budget_type_field: "Hidden",
        budget_category_id_field: "Hidden",
        budget_grouping_field: "Budget grouping",
        budget_category_name_field: "Budget category",
    }
    expenditure_sub_total = [
        budget_type_field,
        budget_grouping_field,
    ]
    expenditure_display_sub_total_column = budget_category_name_field

    expenditure_order_list = [
        budget_type_order_field,
        budget_grouping_order_field,
    ]

    # Project data
    project_columns = {
        project_name_field: "Project",
        project_code_field: "code",
        expenditure_type_order_field: "Hidden",
        expenditure_type_name_field: "Expenditure type",
    }
    project_order_list = [
        project_code_field,
        expenditure_type_order_field,
    ]
    project_sub_total = [
        project_name_field,
    ]
    project_display_sub_total_column = project_code_field

    project_detail_view = [
        'project_details_dit',
        'project_details_group',
        'project_details_directorate',
        'project_details_costcentre',
    ]

    filter_codes = ['', 'group_code', 'directorate_code', 'cost_centre_code']
    filter_selectors = [
        '',
        group_code_field,
        directorate_code_field,
        cost_centre_code_field,
    ]

    hierarchy_columns = [
        group_columns,
        directorate_columns,
        cost_centre_columns,
        cost_centre_columns,
    ]

    hierarchy_sub_total_column = [
        group_name_field,
        directorate_name_field,
        cost_centre_name_field,
        cost_centre_name_field,
    ]

    hierarchy_order_lists = [
        [budget_type_order_field, group_name_field, ],
        [budget_type_order_field, directorate_name_field, ],
        [budget_type_order_field, cost_centre_name_field, ],
        [budget_type_order_field, ]
    ]

    hierarchy_view_link_column = [
        group_name_field,
        directorate_name_field,
        cost_centre_name_field,
    ]

    hierarchy_view = [
        'forecast_group',
        'forecast_directorate',
        'forecast_cost_centre'
    ]

    hierarchy_view_code = [
        group_code_field,
        directorate_code_field,
        cost_centre_code_field,
    ]


    expenditure_view = [
        'expenditure_details_dit',
        'expenditure_details_group',
        'expenditure_details_directorate',
        'expenditure_details_cost_centre',
    ]
    # NAC data
    nac_columns = {
        budget_category_name_field: "Hidden",
        nac_name_field: "Natural Account code",
        nac_code_field: "code",
    }
    nac_sub_total = [
        budget_category_name_field,
    ]
    nac_display_sub_total_column = nac_name_field

    nac_order_list = [
        nac_name_field,
    ]

    # programme details data
    programme_details_dit_columns = {
        programme_name_field: "Hidden",
        expenditure_type_name_field: "Expenditure type",
        group_name_field: "Departmental Group",
        group_code_field: "code",
    }
    programme_details_group_columns = {
        programme_name_field: "Hidden",
        expenditure_type_name_field: "Expenditure type",
        directorate_name_field: "Directorate",
        directorate_code_field: "code",
    }

    programme_details_directorate_columns = {
        programme_name_field: "Hidden",
        expenditure_type_name_field: "Expenditure type",
        cost_centre_name_field: "Cost Centre",
        cost_centre_code_field: "code",
    }

    programme_details_sub_total = [
        programme_name_field,
    ]

    programme_details_display_sub_total_column = expenditure_type_name_field

    programme_details_dit_order_list = [
        group_name_field,
    ]
    programme_details_group_order_list = [
        directorate_name_field,
    ]
    programme_details_directorate_order_list = [
        cost_centre_name_field,
    ]

    programme_details_hierarchy_order_list = [
        programme_details_dit_order_list,
        programme_details_group_order_list,
        programme_details_directorate_order_list,
        '',
    ]

    programme_details_hierarchy_columns = [
        programme_details_dit_columns,
        programme_details_group_columns,
        programme_details_directorate_columns,
        '',
    ]

    programme_details_hierarchy_sub_total_column = [
        group_name_field,
        directorate_name_field,
        cost_centre_name_field,
        '',
    ]


    # Project details views
    project_details_dit_columns = {
        expenditure_type_name_field: "Expenditure type",
        group_name_field: "Departmental Group",
        group_code_field: "code",
    }
    project_details_group_columns = {
        expenditure_type_name_field: "Expenditure type",
        directorate_name_field: "Directorate",
        directorate_code_field: "code",
    }
    project_details_directorate_columns = {
        expenditure_type_name_field: "Expenditure type",
        cost_centre_name_field: "Cost Centre",
        cost_centre_code_field: "code",
    }
    project_details_costcentre_columns = {
        expenditure_type_name_field: "Expenditure type",
        cost_centre_name_field: "Cost Centre",
        cost_centre_code_field: "code",
    }

    project_details_sub_total = [
        expenditure_type_name_field,
    ]

    project_details_dit_order_list = [
        group_name_field,
        expenditure_type_name_field,
    ]
    project_details_group_order_list = [
        directorate_name_field,
        expenditure_type_name_field,
    ]
    project_details_directorate_order_list = [
        cost_centre_name_field,
        expenditure_type_name_field,
    ]

    project_details_costcentre_order_list = [
        expenditure_type_name_field,
    ]

    project_details_hierarchy_order_list = [
        project_details_dit_order_list,
        project_details_group_order_list,
        project_details_directorate_order_list,
        project_details_costcentre_order_list,
    ]

    project_details_hierarchy_columns = [
        project_details_dit_columns,
        project_details_group_columns,
        project_details_directorate_columns,
        project_details_costcentre_columns,
    ]

    project_details_hierarchy_sub_total_column = [
        group_name_field,
        directorate_name_field,
        cost_centre_name_field,
        cost_centre_name_field,
    ]


    DEFAULT_PIVOT_COLUMNS = {
        cost_centre_code_field: "Cost Centre code",
        cost_centre_name_field: "Cost Centre description",
        nac_code_field: "Natural Account code",
        nac_name_field: "Natural Account code description",
        programme_code_field: "Programme code",
        programme_name_field: "Programme code description",
        analysis1_code_field: "Contract code",
        analysis1_name_field: "Contract description",
        analysis2_code_field: "Market code",
        analysis2_name_field: "Market description",
        project_code_field: "Project code",
        project_name_field: "Project description",
    }


    VIEW_FORECAST_DOWNLOAD_COLUMNS = {
        group_name_field: "Group name",
        group_code_field: "Group code",
        directorate_name_field: "Directorate name",
        directorate_code_field: "Directorate code",
        cost_centre_name_field: "Cost Centre name",
        cost_centre_code_field: "Cost Centre code",
        budget_grouping_field: "Budget grouping",
        expenditure_type_name_field: "Expenditure type",
        expenditure_type_description_field: "Expenditure type description",
        budget_type_field: "Budget Type",
        budget_category_name_field: "Budget category",
        budget_nac_field: "Budget/Forecast NAC",
        budget_nac_description_field: "Budget/Forecast NAC description",
        nac_code_field: "PO/Actual NAC",
        nac_name_field: "Natural Account code description",
        nac_expenditure_type_field: "NAC Expenditure type",
        programme_code_field: "Programme code",
        programme_name_field: "Programme code description",
        analysis1_code_field: "Contract code",
        analysis1_name_field: "Contract description",
        analysis2_code_field: "Market code",
        analysis2_name_field: "Market description",
        project_code_field: "Project code",
        project_name_field: "Project description",
    }


    EDIT_KEYS_DOWNLOAD = {
        programme_code_field: 'Programme code',
        programme_name_field: "Programme code Description",
        nac_code_field: 'Natural Account code',
        nac_name_field: "Natural Account Code Description",
        analysis1_code_field: 'Contract Code',
        analysis2_code_field: 'Market Code',
        project_code_field: 'Project Code',
    }


    EDIT_FORECAST_DOWNLOAD_COLUMNS = {
        group_name_field: "Group name",
        group_code_field: "Group code",
        directorate_name_field: "Directorate name",
        directorate_code_field: "Directorate code",
        cost_centre_name_field: "Cost Centre name",
        cost_centre_code_field: "Cost Centre code",
        budget_grouping_field: "Budget Grouping",
        expenditure_type_name_field: "Expenditure type",
        expenditure_type_description_field: "Expenditure type description",
        budget_type_field: "Budget type",
        budget_category_name_field: "Budget Category",
        budget_nac_field: "Budget/Forecast NAC",
        budget_nac_description_field: "Budget/Forecast NAC Description",
        nac_expenditure_type_field: "NAC Expenditure Type",
        analysis1_name_field: "Contract Description",
        analysis2_name_field: "Market Description",
        project_name_field: "Project Description",
    }

    EDIT_FORECAST_DOWNLOAD_ORDER = [
        budget_type_edit_order_field,
        programme_code_field,
        budget_grouping_order_field,
        nac_code_field,
    ]


    MI_REPORT_DOWNLOAD_COLUMNS = {
        cost_centre_code_field: "Cost Centre code",
        nac_code_field: 'Natural Account code',
        programme_code_field: 'Programme code',
        analysis1_code_field: 'Contract Code',
        analysis2_code_field: 'Market Code',
        project_code_field: 'Project Code',
    }




def edit_forecast_order():
    # remove financial_code__ prefix from the
    # fields used in the download order.
    edit_fields = ViewForecastFields()
    order_list = []
    prefix_len = len(financial_code_prefix)
    for elem in edit_fields.EDIT_FORECAST_DOWNLOAD_ORDER:
        order_list.append(elem[prefix_len:])
    return order_list


