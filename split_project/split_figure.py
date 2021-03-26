from django.db import connection

from django.db.models import F

from forecast.models import ForecastMonthlyFigure

from split_project.models import ProjectSplitCoefficient, TemporaryCalculatedValues

def copy_values(period_id):
    # clear the previously calculated values
    #  add  the newly calculated values to the current values
    sql_reset_amount = f"UPDATE forecast_forecastmonthlyfigure  " \
                       f"SET amount=oracle_amount " \
                       f"WHERE financial_period_id = {period_id};"
    sql_update = f"UPDATE forecast_forecastmonthlyfigure " \
                 f"SET amount = amount + c.calculated_amount " \
                 f"FROM split_project_temporarycalculatedvalues c " \
                 f"WHERE forecast_forecastmonthlyfigure.financial_period_id = {period_id} " \
                 f"AND forecast_forecastmonthlyfigure.financial_code_id = c.financial_code_id;"
    with connection.cursor() as cursor:
        cursor.execute(sql_reset_amount)
        cursor.execute(sql_update)


def transfer_value(amount, financial_code_id):
    obj = TemporaryCalculatedValues.objects.create(
        financial_code_id=financial_code_id,
        calculated_amount=amount
    )
    obj.save()

def handle_split_project(financial_period_id):
    # Check that we are splitting actuals
    # Clear the table used to stored the results while doing the calculations
    TemporaryCalculatedValues.objects.all().delete()
    # First, calculate the new values
    coefficient_queryset = ProjectSplitCoefficient.objects.filter(financial_period_id=financial_period_id).order_by('financial_code_from')
    prev_financial_code_from_id = 0
    total_value = 0
    transferred_value = 0
    do_split = False
    print(coefficient_queryset.count())
    for coefficient in coefficient_queryset:
        financial_code_from_id = coefficient.financial_code_from_id
        if prev_financial_code_from_id != financial_code_from_id:
            if do_split:
                # complete the transaction we initiated before
                transfer_value(-transferred_value, prev_financial_code_from_id)
            monthly_figure_queryset = ForecastMonthlyFigure.objects.filter(financial_period_id=financial_period_id,
                                                                           financial_code_id=financial_code_from_id)
            # we cannot transfer money if there is no money in the actuals to be split
            if monthly_figure_queryset.count():
                # Found monthly figure
                do_split = True
                total_value = monthly_figure_queryset.first().oracle_amount
                print(f"total_value = {total_value}")
                if total_value == 0:
                    do_split = False
            else:
                do_split = False
            transferred_value = 0
            prev_financial_code_from_id = financial_code_from_id
        if do_split:
            print(f"coefficient.split_coefficient = {coefficient.split_coefficient}")

            value_to_transfer = total_value * coefficient.split_coefficient
            transferred_value += value_to_transfer
            print(f"value_to_transfer {value_to_transfer}, transferred_value = {transferred_value}")
            transfer_value(value_to_transfer, coefficient.financial_code_to_id)
    #  To do: Raise error if the money transferred is more than the money available

    # processed all the rows, copy the last value
    if do_split:
        transfer_value(-transferred_value, prev_financial_code_from_id)

    # The next two steps use raw sql, for speed
    copy_values(financial_period_id)
