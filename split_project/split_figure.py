from django.db.models import F

from forecast.models import ForecastMonthlyFigure

from split_project.models import ProjectSplitCoefficient, TemporaryCalculatedValues

def transfer_value(amount, financial_code):
    TemporaryCalculatedValues.objects.create(
        financial_code=financial_code,
        calculated_amount=amount
    )


def handle_split_project(financial_period_id):
    # Clear the table with the results
    TemporaryCalculatedValues.objects.filter(financial_period_id=financial_period_id).delete()
    # First, calculate the new values
    coefficient_queryset = ProjectSplitCoefficient.objects.filter(financial_period_id=financial_period_id).order_by('financial_code_from')
    prev_financial_code_from = None
    total_value = 0
    transferred_value = 0
    do_split = False
    for coefficient in coefficient_queryset:
        financial_code_from = coefficient.financial_code_from
        if prev_financial_code_from != financial_code_from:
            if do_split:
                # complete the transaction we initiated before
                transfer_value(-transferred_value, prev_financial_code_from)
            monthly_figure_queryset = ForecastMonthlyFigure.objects.filter(financial_period_id=financial_period_id, financial_code=financial_code_from)
            # we cannot transfer money if there is no money in the actuals to be split
            if monthly_figure_queryset.count():
                do_split = True
                total_value = monthly_figure_queryset.first().oracle_amount
                if total_value == 0:
                    do_split = False
            else:
                do_split = False
            transferred_value = 0
            prev_financial_code_from = financial_code_from
        if do_split:
            value_to_transfer = total_value * coefficient.split_coefficient
            transferred_value += value_to_transfer
            transfer_value(value_to_transfer, coefficient.financial_code_to)
    #  To do: Raise error if the money transferred is more than the money available

    # processed all the rows, copy the last value
    if do_split:
        transfer_value(-transferred_value, prev_financial_code_from)

    # The next two steps use raw sql, for speed
    # Next, clear the previously calculated values
    ForecastMonthlyFigure.objects.filter(financial_period_id=financial_period_id).update(amount=F("oracle_amount"))

    # last, add  the newly calculated values to the current values
    pass