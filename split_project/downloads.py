from core.utils.export_helpers import export_to_excel

from forecast.models import FinancialPeriod
from forecast.utils.export_helpers import get_obj_value

from split_project.import_project_percentage import EXPECTED_PERCENTAGE_HEADERS
from split_project.models import ProjectSplitCoefficient


def export_template(queryset):
    yield EXPECTED_PERCENTAGE_HEADERS


def create_template():
    title = "Percentage split"
    return export_to_excel(None, export_template, title)


def export_percentage(queryset, fields):
    yield list(
        fields.values()
    ) + FinancialPeriod.financial_period_info.period_display_all_list()
    for obj in queryset:
        apr = get_obj_value(obj, "Apr")
        may = get_obj_value(obj, "May")
        jun = get_obj_value(obj, "Jun")
        jul = get_obj_value(obj, "Jul")
        aug = get_obj_value(obj, "Aug")
        sep = get_obj_value(obj, "Sep")
        oct = get_obj_value(obj, "Oct")
        nov = get_obj_value(obj, "Nov")
        dec = get_obj_value(obj, "Dec")
        jan = get_obj_value(obj, "Jan")
        feb = get_obj_value(obj, "Feb")
        mar = get_obj_value(obj, "Mar")
        adj1 = get_obj_value(obj, "Adj1")
        adj2 = get_obj_value(obj, "Adj2")
        adj3 = get_obj_value(obj, "Adj3")
        data_list = []
        for f in fields.keys():
            data_list.append(obj[f])
        yield data_list + [
            apr / 10000,
            may / 10000,
            jun / 10000,
            jul / 10000,
            aug / 10000,
            sep / 10000,
            oct / 10000,
            nov / 10000,
            dec / 10000,
            jan / 10000,
            feb / 10000,
            mar / 10000,
            adj1 / 10000,
            adj2 / 10000,
            adj3 / 10000,
        ]


def create_percentage_download():
    title = "Percentage split"

    columns = {
        "financial_code_to__cost_centre__cost_centre_code":
            "Cost centre code",
        "financial_code_to__cost_centre__cost_centre_name":
            "Cost centre description",
        "financial_code_to__natural_account_code__natural_account_code":
            "Natural Account code",
        "financial_code_to__natural_account_code__natural_account_code_description":
            "Natural Account description",
        "financial_code_to__programme__programme_code":
            "Programme code",
        "financial_code_to__programme__programme_description":
            "Programme description",
        "financial_code_to__analysis1_code__analysis1_code":
            "Contract Code",
        "financial_code_to__analysis1_code__analysis1_description":
            "Contract description",
        "financial_code_to__analysis2_code__analysis2_code":
            "Market Code",
        "financial_code_to__analysis2_code__analysis2_description":
            "Market description",
        "financial_code_to__project_code__project_code":
            "Project Code",
        "financial_code_to__project_code__project_description":
            "Project description",
    }

    return export_to_excel(
        ProjectSplitCoefficient.pivot.pivot_data(columns),
        export_percentage,
        title,
        columns,
    )
