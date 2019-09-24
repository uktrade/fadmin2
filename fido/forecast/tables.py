from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Max

import django_tables2 as tables

from .models import FinancialPeriod


def actual_month():
    m = FinancialPeriod.objects.filter(actual_loaded=True).aggregate(Max('financial_period_code'))
    return m['financial_period_code__max'] or 0


class SummingFooterCol(tables.Column):
    # display 0 for null value instead of a dash
    default = 0
    tot_value = 0

    def render(self, value):
        v = (value or 0)
        self.tot_value += v
        # return '{:0.2f}'.format(value)
        return intcomma(v)

    def value(self, record, value):
        return float(value or 0)

    # attrs = {'td': {'class': 'text-right'},
    #          'th': {'class': 'text-right other-class'},
    #          'tf': {'class': 'text-right font-weight-bold'}}

    def render_footer(self, bound_column, table):
        return intcomma(self.tot_value)


class SummingMonthCol(SummingFooterCol):
    """It expects a list of month as first argument.
    Used to calculate and display year to date, full year, etc"""

    def calc_value(self, record):
        val = sum(record[m] for m in self.month_list if record[m] is not None)
        return val or 0

    def render(self, value, record):
        val = self.calc_value(record)
        self.tot_value += val
        return intcomma(val)

    def value(self, record, value):
        val = self.calc_value(record)
        return float(val)

    def __init__(self, month_list, *args, **kwargs):
        self.month_list = month_list
        super().__init__(*args, **kwargs)


class ForecastTable(tables.Table):
    """Define the month columns format and their footer.
    Used every time we need to display a forecast"""

    # full list of month, in the correct order for the financial year
    # I don't like hardcoded strings, but the month names are not going to change, and anyway
    # they must match the columns defined below
    full_year = ['apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar']

    budg = SummingFooterCol('Budget', empty_values=())
    apr = SummingFooterCol('April', empty_values=())
    may = SummingFooterCol('May', empty_values=())
    jun = SummingFooterCol('June', empty_values=())
    jul = SummingFooterCol('July', empty_values=())
    aug = SummingFooterCol('August', empty_values=())
    sep = SummingFooterCol('September', empty_values=())
    oct = SummingFooterCol('October', empty_values=())
    nov = SummingFooterCol('November', empty_values=())
    dec = SummingFooterCol('December', empty_values=())
    jan = SummingFooterCol('January', empty_values=())
    feb = SummingFooterCol('February', empty_values=())
    mar = SummingFooterCol('March', empty_values=())

    def __init__(self, column_dict={}, *args, **kwargs):
        extra_col = [(k, tables.Column(v)) for (k, v) in column_dict.items()]

        column_list = column_dict.keys()
        actual_period = actual_month()
        actual_month_list = self.full_year[:actual_period]
        forecast_month_list = self.full_year[actual_period:]
        forecast_month_col = [ tables.Column(v) for v in forecast_month_list]

        extra_col.extend([('year_to_date', SummingMonthCol(actual_month_list,
                                                           'Year to Date', empty_values=())),
                          ('year_total', SummingMonthCol(self.full_year, 'Year Total', empty_values=()))])
        super().__init__(extra_columns=extra_col,
                         sequence=column_list, *args, **kwargs)
        for month in forecast_month_list:
            col = self.columns[month]
            col.column.attrs = {
                            'tf': {'class': 'forecast_class'}
                            }

    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        empty_text = ''
        attrs = {"class": "table-bordered table-condensed small-font"}