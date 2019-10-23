from django.conf import settings

from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    BudgetType,
    NaturalCode,
    ProgrammeCode,
    ProjectCode
)

from core.metamodels import TimeStampedModel
from core.models import FinancialYear
from core.myutils import get_current_financial_year
from core.utils import GRAN_TOTAL_CLASS, SUB_TOTAL_CLASS
from costcentre.models import CostCentre

from django.db import models

from django.db.models import Max

# https://github.com/martsberger/django-pivot/blob/master/django_pivot/pivot.py
from django_pivot.pivot import pivot


class SubTotalFieldDoesNotExistError(Exception):
    pass


class SubTotalFieldNotSpecifiedError(Exception):
    pass


class CalcForecastExpenditureType(models.Model):
    """The expenditure type is a combination of the economic budget (NAC) and the budget type (Programme).
    As such, it can only be defined for a forecast row, when both NAC and programme are defined.
    This table is prepulated with the information needed to calculate the expenditure_type.
    """
    nac_economic_budget_code = models.CharField(max_length=255, verbose_name='economic budget code')
    programme_budget_type = models.ForeignKey(BudgetType, on_delete=models.CASCADE)
    forecast_expenditure_type_fk = models.ForeignKey(ForecastExpenditureType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('nac_economic_budget_code',
                           'programme_budget_type')


class ForecastExpenditureType(models.Model):
    """The expenditure type is a combination of the economic budget (NAC) and the budget type (Programme).
    As such, it can only be defined for a forecast row, when both NAC and programme are defined.
    This table is prepulated with the information needed to calculate the expenditure_type.
    """
    forecast_expenditure_type_name = models.CharField(max_length=100)
    forecast_expenditure_type_description = models.CharField(max_length=100)
    forecast_expenditure_type_display_order = models.IntegerField()

    def __str__(self):
        return self.forecast_expenditure_type_name


class FinancialPeriodManager(models.Manager):
    def period_display_list(self):
        return (list(self.get_queryset().filter(display_figure=True).values_list('period_short_name', flat=True)))

    def actual_month(self):
        m = self.get_queryset().filter(actual_loaded=True).aggregate(Max('financial_period_code'))
        return m['financial_period_code__max'] or 0

    def actual_month_list(self):
        return self.period_display_list()[:self.actual_month()]

    def periods(self):
        return self.get_queryset().filter(display_figure=True).values_list('period_short_name', 'period_long_name')


class FinancialPeriod(models.Model):
    """Financial periods: correspond to month, but there are 3 extra periods at the end"""
    financial_period_code = models.IntegerField(primary_key=True)  # April = 1
    period_long_name = models.CharField(max_length=20)
    period_short_name = models.CharField(max_length=10)
    period_calendar_code = models.IntegerField()  # January = 1
    # use a flag to indicate if the actuals have been uploaded instead of relying on the date
    # the actuals are manually uploaded, so it is not garanteed on which date they are uploaded
    actual_loaded = models.BooleanField(default=False)
    display_figure = models.BooleanField(default=True)

    objects = models.Manager()  # The default manager.
    financial_period_info = FinancialPeriodManager()

    class Meta:
        ordering = ['financial_period_code']

    def __str__(self):
        return self.period_long_name


class FinancialCode(models.Model):
    """Contains the members of Chart of Account needed to create a unique key"""
    programme = models.ForeignKey(ProgrammeCode, on_delete=models.PROTECT)
    cost_centre = models.ForeignKey(CostCentre, on_delete=models.PROTECT)
    natural_account_code = models.ForeignKey(NaturalCode, on_delete=models.PROTECT)
    analysis1_code = models.ForeignKey(Analysis1, on_delete=models.PROTECT, blank=True, null=True)
    analysis2_code = models.ForeignKey(Analysis2, on_delete=models.PROTECT, blank=True, null=True)
    project_code = models.ForeignKey(ProjectCode, on_delete=models.PROTECT, blank=True, null=True)
    # The following field is calculated from programme and NAC.
    forecast_expenditure_type = models.ForeignKey(ForecastExpenditureType, on_delete=models.PROTECT, default=1)

    def save(self, *args, **kwargs):
        # Override save to calculate the forecast_expenditure_type.
        if self.pk is None:
            # calculate the forecast_expenditure_type
            nac_economic_budget_code = self.natural_account_code.account_L5_code.economic_budget_code
            programme_budget_type = self.programme.budget_type_fk

            calc_forecast = CalcForecastExpenditureType.objects.filter(
                programme_budget_type=programme_budget_type,
                nac_economic_budget_code=nac_economic_budget_code,
            )

            self.forecast_expenditure_type = calc_forecast[0].forecast_expenditure_type_fk

        super(FinancialCode, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Budget(FinancialCode, TimeStampedModel):
    """Used to store the budgets for the financial year. The data is not profiled"""
    id = models.AutoField('Budget ID', primary_key=True)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT)
    budget = models.BigIntegerField(default=0)

    class Meta:
        unique_together = ('programme',
                           'cost_centre',
                           'natural_account_code',
                           'analysis1_code',
                           'analysis2_code',
                           'project_code',
                           'financial_year')

    def __str__(self):
        return str(self.cost_centre) + '--' \
               + str(self.programme) + '--' \
               + str(self.natural_account_code) + '--' \
               + str(self.analysis1_code) + '--' \
               + str(self.analysis2_code) + '--' \
               + str(self.project_code) + '--' \
               + str(self.financial_year)


class PivotManager(models.Manager):
    """Managers returning the data in Monthly figures pivoted"""
    default_columns = {
        'cost_centre__cost_centre_code': 'Cost Centre Code',
        'cost_centre__cost_centre_name': 'Cost Centre Description',
        'natural_account_code__natural_account_code': 'Natural Account Code',
        'natural_account_code__natural_account_code_description': 'Natural Account Code Description',
        'programme__programme_code': 'Programme Code',
        'programme__programme_description': 'Programme Description',
        'project_code__project_code': 'Project Code',
        'project_code__project_description': 'Project Description',
    }

    def output_row_to_table(self, table, row, style_name='', level=99):
        #     Add the stile entry to the dictionary
        #     add the resulting dictionary to the list
        # if style_name != '':
        #     style_name = '{}-{}'.format(style_name, level)
        row['row_type'] = style_name
        table.append(row)

    def add_row_to_subtotal(self, row_from, sub_total):
        for period in self.period_list:
            sub_total[period] += row_from[period]

    def clear_row(self, row):
        for period in self.period_list:
            row[period] = 0

    def subtotal_data(
        self,
        display_total_column,
        subtotal_columns,
        data_columns,
        filter_dict={},
        year=0,
        order_list=[],
    ):
        # If requesting a subtotal, the list of columns must be specified
        if not subtotal_columns:
            raise SubTotalFieldNotSpecifiedError("Sub-total field not specified")

        if not all(elem in [*data_columns] for elem in subtotal_columns):
            raise SubTotalFieldDoesNotExistError("Sub-total column does not exist")

        if display_total_column not in [*data_columns]:
            raise SubTotalFieldDoesNotExistError("Display sub-total column does not exist")

        data_returned = self.pivotdata(
            data_columns,
            filter_dict,
            year,
            order_list
        )

        result_table = []
        pivot_data = list(data_returned)
        if not pivot_data:
            return []
        # The subtotals are passed in from the outer totals
        # for calculation, it is easier to call subtotal 0 the innermost subtotal
        subtotal_columns.reverse()
        first_row = pivot_data.pop(0)

        self.output_row_to_table(
            result_table,
            first_row,
            ''
        )
        full_list = list(FinancialPeriod.objects.values_list('period_short_name', flat=True))
        # remove missing periods (like Adj1, etc from the list used to add the periods together.
        self.period_list = [value for value in full_list if value in first_row.keys()]
        # import pdb;
        # pdb.set_trace()
        # Initialise the structure required
        # a dictionary with the previous value of the columns to be sub-totalled
        # a dictionary of subtotal dictionaries, with an extra entry for the final total (gran total)
        sub_total_row = {k: (v if k in self.period_list else ' ') for k, v in first_row.items()}
        previous_values = {field_name: first_row[field_name] for field_name in subtotal_columns}
        # initialise all the subtotals, and add an extra row for the final total (gran total)
        subtotals = {field_name: sub_total_row.copy() for field_name in subtotal_columns}
        sub_total_levels = len(subtotals)
        subtotals['Gran_Total'] = sub_total_row.copy()
        output_subtotal = {field_name: False for field_name in subtotal_columns}
        for current_row in pivot_data:
            subtotal_time = False
            # check if we need a subtotal.
            # we check from the inner subtotal
            for column in subtotal_columns:
                if current_row[column] != previous_values[column]:
                    subtotal_time = True
                    output_subtotal[column] = True
            if subtotal_time:
                do_subtotal = False
                # Check the subtotals, from the outer subtotal to the inner one.
                # if an outer subtotal is needed, all the inner one are needed too
                for column in subtotal_columns[::-1]:
                    if output_subtotal[column]:
                        # this trigger the subtotals in the inner fields.
                        do_subtotal = True
                    else:
                        output_subtotal[column] = do_subtotal

                for column in subtotal_columns:
                    if output_subtotal[column]:
                        subtotal_row = subtotals[column].copy()
                        level = subtotal_columns.index(column)
                        subtotal_row[display_total_column] = 'Total {}'.format(previous_values[column])
                        for out_total in subtotal_columns[level + 1:]:
                            subtotal_row[display_total_column] = '{} {}'.format(
                                subtotal_row[display_total_column],
                                previous_values[out_total])
                        self.output_row_to_table(result_table, subtotal_row, SUB_TOTAL_CLASS, sub_total_levels - level)
                        self.clear_row(subtotals[column])
                        previous_values[column] = current_row[column]
                        output_subtotal[column] = False
                    else:
                        break

            for k, totals in subtotals.items():
                self.add_row_to_subtotal(current_row, totals)

            self.output_row_to_table(result_table, current_row)

        # output all the subtotals, because it is finished
        for column in subtotal_columns:
            level = subtotal_columns.index(column)
            caption = 'Total {}'.format(previous_values[column])
            for out_total in subtotal_columns[level + 1:]:
                caption = '{} {}'.format(
                    caption,
                    previous_values[out_total])
            subtotals[column][display_total_column] = caption
            self.output_row_to_table(result_table, subtotals[column], SUB_TOTAL_CLASS, sub_total_levels - level)
        subtotals['Gran_Total'][display_total_column] = 'Total Managed Expenditure'
        self.output_row_to_table(result_table, subtotals['Gran_Total'], GRAN_TOTAL_CLASS, 0)

        return result_table

    def pivotdata(self, columns={}, filter_dict={}, year=0, order_list=[]):
        if year == 0:
            year = get_current_financial_year()
        if columns == {}:
            columns = self.default_columns

        q1 = self.get_queryset().filter(
            financial_year=year,
            **filter_dict
        ).order_by(*order_list)

        return pivot(
            q1,
            columns,
            'financial_period__period_short_name',
            'amount'
        )


class MonthlyFigure(FinancialCode, TimeStampedModel):
    """It contains the forecast and the actuals.
    The current month defines what is Actual and what is Forecast"""
    id = models.AutoField('Monthly ID', primary_key=True)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT)
    financial_period = models.ForeignKey(FinancialPeriod, on_delete=models.PROTECT)
    # The figures are stored ar pence, to avoid rounding problems.
    # Some formatting will take care of displaying the figures as pounds only
    amount = models.BigIntegerField(default=0)

    objects = models.Manager()  # The default manager.
    pivot = PivotManager()

    class Meta:
        unique_together = (
            'programme',
            'cost_centre',
            'natural_account_code',
            'analysis1_code',
            'analysis2_code',
            'project_code',
            'financial_year',
            'financial_period',
        )

    def __str__(self):
        return str(self.cost_centre) + '--' \
               + str(self.programme) + '--' \
               + str(self.natural_account_code) + '--' \
               + str(self.analysis1_code) + '--' \
               + str(self.analysis2_code) + '--' \
               + str(self.project_code) + '--' \
               + str(self.financial_year) + '--' \
               + str(self.financial_period)


class OSCARReturn(models.Model):
    """Used for downloading the Oscar return. Mapped to a view in the database, because the query is too complex"""
    # The view is created by the migration 0016_recreate_oscar_view.py
    # TODO Change the database view to return figures in thousands. At the moment the figures are in pence.
    row_number = models.BigIntegerField()
    account_l5_code = models.ForeignKey(
        'treasuryCOA.L5Account',
        on_delete=models.PROTECT,
        db_column='account_l5_code'
    )
    sub_segment_code = models.CharField(max_length=8, primary_key=True)
    sub_segment_long_name = models.CharField(max_length=255)
    apr = models.BigIntegerField(default=0)
    may = models.BigIntegerField(default=0)
    jun = models.BigIntegerField(default=0)
    jul = models.BigIntegerField(default=0)
    aug = models.BigIntegerField(default=0)
    sep = models.BigIntegerField(default=0)
    oct = models.BigIntegerField(default=0)
    nov = models.BigIntegerField(default=0)
    dec = models.BigIntegerField(default=0)
    jan = models.BigIntegerField(default=0)
    feb = models.BigIntegerField(default=0)
    mar = models.BigIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'forecast_oscarreturn'
        ordering = ['sub_segment_code']

# Query created in the database to return the info for the OSCAR return
# DROP VIEW "forecast_oscarreturn";
# CREATE VIEW "forecast_oscarreturn" as
#
# SELECT ROW_NUMBER () OVER (ORDER BY "treasurySS_subsegment"."sub_segment_code"),
# coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id") account_l5_code
# ,
# "treasurySS_subsegment"."sub_segment_code" , "treasurySS_subsegment"."sub_segment_long_name" ,
#
# SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Apr' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "apr", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Aug' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "aug", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Dec' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "dec", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Feb' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "feb", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Jan' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "jan", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Jul' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "jul", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Jun' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "jun", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Mar' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "mar", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'May' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "may", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Nov' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "nov", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Oct' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "oct", SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Sep' THEN "forecast_monthlyfigure"."amount" ELSE NULL END) AS "sep"
#
# FROM "forecast_monthlyfigure" LEFT OUTER JOIN "chartofaccountDIT_naturalcode" ON ("forecast_monthlyfigure"."natural_account_code_id" = "chartofaccountDIT_naturalcode"."natural_account_code") INNER JOIN "costcentre_costcentre" ON ("forecast_monthlyfigure"."cost_centre_id" = "costcentre_costcentre"."cost_centre_code") INNER JOIN "costcentre_directorate" ON ("costcentre_costcentre"."directorate_id" = "costcentre_directorate"."directorate_code") INNER JOIN "costcentre_departmentalgroup" ON ("costcentre_directorate"."group_id" = "costcentre_departmentalgroup"."group_code") INNER JOIN "chartofaccountDIT_programmecode" ON ("forecast_monthlyfigure"."programme_id" = "chartofaccountDIT_programmecode"."programme_code") INNER JOIN "forecast_financialperiod" ON ("forecast_monthlyfigure"."financial_period_id" = "forecast_financialperiod"."financial_period_code")
# LEFT OUTER JOIN "treasurySS_subsegment" ON ("costcentre_departmentalgroup"."treasury_segment_fk_id" = "treasurySS_subsegment"."Segment_code_id"
# AND "chartofaccountDIT_programmecode"."budget_type_fk_id" = "treasurySS_subsegment"."dit_budget_type_id")
# INNER JOIN "core_financialyear" ON ("forecast_monthlyfigure"."financial_year_id" = "core_financialyear"."financial_year")
# WHERE "core_financialyear"."current" = TRUE
# GROUP BY coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id"),
# "treasurySS_subsegment"."sub_segment_code" ;
