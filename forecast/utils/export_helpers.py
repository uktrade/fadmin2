from django.http import HttpResponse

import openpyxl

from core.utils import today_string
from core.exportutils import (
    EXC_TAB_NAME_LEN,
    EXCEL_TYPE,
)


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
    filename = title + today_string() + " " + ".xlsx"
    resp["Content-Disposition"] = "attachment; filename=" + filename
    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    # Truncate the tab name to the maximum lenght permitted by Excel
    ws.title = title[:EXC_TAB_NAME_LEN]
    for row in forecast_query_iterator(queryset, columns_dict):
        ws.append(row)
    wb.save(resp)
    return resp
