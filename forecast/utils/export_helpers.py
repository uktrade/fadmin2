from django.http import HttpResponse

import openpyxl

from openpyxl import Workbook
from openpyxl.utils import (
    get_column_letter, 
    column_index_from_string
)

from core.utils import today_string
from core.exportutils import (
    EXC_TAB_NAME_LEN,
    EXCEL_TYPE,
)

from forecast.models import FinancialPeriod

EDIT_BUDGET_COL = "F"
EDIT_FIRST_MONTH_COL = "G"
EDIT_LAST_MONTH_COL = "R"
EDIT_YEAR_TO_DATE_COL = "S"
EDIT_YEAR_TOTAL_COL = "T"
EDIT_OVERSPEND_COL = "U"

VIEW_BUDGET_COL = "X"
VIEW_FIRST_MONTH_COL = "Y"
VIEW_LAST_MONTH_COL = "AJ"
VIEW_YEAR_TO_DATE_COL = "AK"
VIEW_YEAR_TOTAL_COL = "AL"
VIEW_OVERSPEND_COL = "AM"


MONTH_HEADERS = [
    'Budget',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
    'Jan',
    'Feb',
    'Mar',
    'Year to Date',
    'Year Total',
    'Underspend/Overspend',
]


def forecast_query_iterator(queryset, columns_dict):
    for obj in queryset:
        row = []
        for field in columns_dict.keys():
            val = obj[field]
            if val is None:
                val = ""
            row.append(val)
        row.append(obj['Budget']/100)
        row.append(obj['Apr']/100)
        row.append(obj['May']/100)
        row.append(obj['Jun']/100)
        row.append(obj['Jul']/100)
        row.append(obj['Aug']/100)
        row.append(obj['Sep']/100)
        row.append(obj['Oct']/100)
        row.append(obj['Nov']/100)
        row.append(obj['Dec']/100)
        row.append(obj['Jan']/100)
        row.append(obj['Feb']/100)
        row.append(obj['Mar']/100)
        yield row


def format_numbers(ws, row, start):
    for c in range(start, start+16):
        ws[f'{get_column_letter(c)}{row}'].number_format = '#,##0.00'


def export_query_to_excel(queryset, columns_dict, title):
    resp = HttpResponse(content_type=EXCEL_TYPE)
    filename = f'{title}  {today_string()} .xlsx'
    resp["Content-Disposition"] = "attachment; filename=" + filename
    wb = Workbook()
    ws = wb.get_active_sheet()
    # Truncate the tab name to the maximum lenght permitted by Excel
    ws.title = f'{title} {today_string()}'[:EXC_TAB_NAME_LEN]
    ws.append(create_headers(columns_dict, {}))

    row_count = 1
    first_actual = VIEW_FIRST_MONTH_COL
    last_actual = last_actual_cell(first_actual)
    for row in forecast_query_iterator(queryset, columns_dict):
        ws.append(row)
        row_count += 1
        ws[f'{VIEW_FIRST_MONTH_COL}{row_count}'].number_format = '#,##0.00'
        ws[f'{VIEW_BUDGET_COL}{row_count}'].number_format = '#,##0.00'
        if last_actual:
            ws[f'{VIEW_YEAR_TO_DATE_COL}{row_count}'].value = \
                f'=SUM({first_actual}{row_count}:{last_actual}{row_count})'
        ws[f'{VIEW_YEAR_TOTAL_COL}{row_count}'].value = \
            f'=SUM({VIEW_FIRST_MONTH_COL}{row_count}:{VIEW_LAST_MONTH_COL}{row_count})'
        ws[f'{VIEW_OVERSPEND_COL}{row_count}'].value = \
            f'=({VIEW_BUDGET_COL}{row_count}-{VIEW_YEAR_TOTAL_COL}{row_count})'
        format_numbers (ws, row_count, column_index_from_string(VIEW_BUDGET_COL))

    wb.save(resp)
    return resp


def edit_forecast_query_iterator(queryset, keys_dict, columns_dict):
    for obj in queryset:
        row = []
        for field in keys_dict.keys():
            val = obj[field]
            if val is None:
                val = ""
            row.append(val)
        row.append(obj['Budget']/100)
        row.append(obj['Apr']/100)
        row.append(obj['May']/100)
        row.append(obj['Jun']/100)
        row.append(obj['Jul']/100)
        row.append(obj['Aug']/100)
        row.append(obj['Sep']/100)
        row.append(obj['Oct']/100)
        row.append(obj['Nov']/100)
        row.append(obj['Dec']/100)
        row.append(obj['Jan']/100)
        row.append(obj['Feb']/100)
        row.append(obj['Mar']/100)
        row.append('')
        row.append('')
        row.append('')
        for field in columns_dict.keys():
            val = obj[field]
            if val is None:
                val = ""
            row.append(val)
        yield row


def create_headers(keys_dict, columns_dict):
    k = list(keys_dict.values())
    l = list(columns_dict.values())
    k.extend(MONTH_HEADERS)
    k.extend(l)
    return k


def last_actual_cell(col):
    actual_month = FinancialPeriod.financial_period_info.actual_month()
    if actual_month:
         return(get_column_letter(column_index_from_string(col) + actual_month))
    return 0


def export_edit_to_excel(queryset, key_dict, columns_dict, title):
    resp = HttpResponse(content_type=EXCEL_TYPE)
    filename = f'{title}  {today_string()} .xlsx'
    resp["Content-Disposition"] = "attachment; filename=" + filename
    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    # Truncate the tab name to the maximum lenght permitted by Excel
    ws.title = f'{title} {today_string()}'[:EXC_TAB_NAME_LEN]
    row_count = 1
    first_actual = EDIT_FIRST_MONTH_COL
    last_actual = last_actual_cell(first_actual)

    ws.append(create_headers(key_dict, columns_dict))
    for data_row in edit_forecast_query_iterator(queryset, key_dict, columns_dict):
        ws.append(data_row)
        row_count += 1
        # Formula for Year To Date. Don't use it if there are no actuals
        if last_actual:
            ws[f'{EDIT_YEAR_TO_DATE_COL}{row_count}'].value = \
                f'=SUM({first_actual}{row_count}:{last_actual}{row_count})'
        else:
            ws[f'{EDIT_YEAR_TO_DATE_COL}{row_count}'].value = 0
        # Formula for calculating the full year
        ws[f'{EDIT_YEAR_TOTAL_COL}{row_count}'].value = \
            f'=SUM({EDIT_FIRST_MONTH_COL}{row_count}:{EDIT_LAST_MONTH_COL}{row_count})'
        # Formula for overspend/underspend
        ws[f'{EDIT_OVERSPEND_COL}{row_count}'].value = \
            f'=({EDIT_BUDGET_COL}{row_count}-{EDIT_YEAR_TOTAL_COL}{row_count})'
        format_numbers (ws, row_count, column_index_from_string(EDIT_BUDGET_COL))

    wb.save(resp)
    return resp


