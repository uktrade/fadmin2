from django.contrib.auth.decorators import user_passes_test

from core.exportutils import export_to_excel
from core.utils import today_string

from forecast.models import OSCARReturn
from forecast.utils.access_helpers import (
    can_download_oscar,
)


def export_oscarreport_iterator(queryset):
    yield [
        "Row",
        "Organisation",
        "Organisation Alias",
        "COA",
        "COA Alias",
        "Sub Segment",
        "Sub Segment Alias",
        "Adj Type",
        "AdjType Alias",
        "APR",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC",
        "JAN",
        "FEB",
        "MAR",
    ]
    for obj in queryset:
        try:
            yield [
                obj.row_number,
                "UKT013",
                "UK TRADE & INVESTMENT",
                obj.account_l5_code.account_l5_code if obj.account_l5_code else "",
                obj.account_l5_code.account_l5_long_name if obj.account_l5_code else "",
                obj.sub_segment_code,
                obj.sub_segment_long_name,
                "TYPE_INYEAR",
                "IN-YEAR RETURN",
                obj.apr,
                obj.may,
                obj.jun,
                obj.jul,
                obj.aug,
                obj.sep,
                obj.oct,
                obj.nov,
                obj.dec,
                obj.jan,
                obj.feb,
                obj.mar,
            ]
        except OSCARReturn.account_l5_code.RelatedObjectDoesNotExist:
            pass


@user_passes_test(can_download_oscar, login_url='index')
def create_oscar_report():
    title = f"OSCAR {today_string()}"
    queryset = OSCARReturn.objects.all()
    return export_to_excel(queryset, export_oscarreport_iterator, title)
