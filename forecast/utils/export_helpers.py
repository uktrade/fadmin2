from django.http import HttpResponse

import openpyxl

from core.utils import today_string
from core.exportutils import (
    EXC_TAB_NAME_LEN,
    EXCEL_TYPE,
)

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
    month_list = ['Budget',
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
                  'Mar']
    l = list(columns_dict.values())
    l.extend(month_list)
    yield l

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


def export_query_to_excel(queryset, columns_dict, title):
    resp = HttpResponse(content_type=EXCEL_TYPE)
    filename = f'{title}  {today_string()} .xlsx'
    resp["Content-Disposition"] = "attachment; filename=" + filename
    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    # Truncate the tab name to the maximum lenght permitted by Excel
    ws.title = f'{title} {today_string()}'[:EXC_TAB_NAME_LEN]
    for row in forecast_query_iterator(queryset, columns_dict):
        ws.append(row)
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


APRIL_COL = "G"

def create_headers(keys_dict, columns_dict):
    k = list(keys_dict.values())
    l = list(columns_dict.values())
    k.extend(MONTH_HEADERS)
    k.extend(l)
    return k

def last_actual_cell(col):
    return 'K'

def export_edit_to_excel(queryset, key_dict, columns_dict, title):
    resp = HttpResponse(content_type=EXCEL_TYPE)
    filename = f'{title}  {today_string()} .xlsx'
    resp["Content-Disposition"] = "attachment; filename=" + filename
    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    # Truncate the tab name to the maximum lenght permitted by Excel
    ws.title = f'{title} {today_string()}'[:EXC_TAB_NAME_LEN]
    row_count = 1
    first_actual = 'G'
    last_actual = 'K'

    ws.append(create_headers(key_dict, columns_dict))
    for data_row in edit_forecast_query_iterator(queryset, key_dict, columns_dict):
        ws.append(data_row)
        row_count += 1

        ws[f'S{row_count}'].value = f'=SUM({first_actual}{row_count}:{last_actual}{row_count})'
        ws[f'T{row_count}'].value = f'=SUM(G{row_count}:R{row_count})'
        ws[f'U{row_count}'].value = f'=(F{row_count}-T{row_count})'

    wb.save(resp)
    return resp


