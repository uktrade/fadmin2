from django.db import migrations

fields = [
    "financial_period_code",
    "period_long_name",
    "period_short_name",
    "period_calendar_code",
]

periods = [
    [1, "April", "Apr", 4],
    [2, "May", "May", 5],
    [3, "June", "Jun", 6],
    [4, "July", "Jul", 7],
    [5, "August", "Aug", 8],
    [6, "September", "Sep", 9],
    [7, "October", "Oct", 10],
    [8, "November", "Nov", 11],
    [9, "December", "Dec", 12],
    [10, "January", "Jan", 1],
    [11, "February", "Feb", 2],
    [12, "March", "Mar", 3],
    [13, "Adjustment 1", "Adj1", 0],
    [14, "Adjustment 2", "Adj2", 0],
    [15, "Adjustment 3", "Adj3", 0],
]


def populate_period(apps, schema_editor):
    PeriodModel = apps.get_model("forecast", "FinancialPeriod")
    for l in periods:
        d = dict(zip(fields, l))
        obj, created = PeriodModel.objects.get_or_create(**d)


def create_forecast_expenditure_types(apps, schema_editor):
    ForecastExpenditureType = apps.get_model("forecast", "ForecastExpenditureType")
    BudgetType = apps.get_model("chartofaccountDIT", "BudgetType")

    del_type = BudgetType.objects.get(budget_type_key="DEL")
    ame_type = BudgetType.objects.get(budget_type_key="AME")
    admin_type = BudgetType.objects.get(budget_type_key="ADMIN")

    ForecastExpenditureType.objects.create(
        forecast_expenditure_type_name="Capital",
        forecast_expenditure_type_description="Capital",
        forecast_expenditure_type_display_order=3,
        nac_economic_budget_code="CAPITAL",
        programme_budget_type=del_type,
    ).save()

    ForecastExpenditureType.objects.create(
        forecast_expenditure_type_name="Capital",
        forecast_expenditure_type_description="Capital",
        forecast_expenditure_type_display_order=3,
        nac_economic_budget_code="CAPITAL",
        programme_budget_type=ame_type,
    ).save()

    ForecastExpenditureType.objects.create(
        forecast_expenditure_type_name="Capital",
        forecast_expenditure_type_description="Capital",
        forecast_expenditure_type_display_order=3,
        nac_economic_budget_code="CAPITAL",
        programme_budget_type=admin_type,
    ).save()

    ForecastExpenditureType.objects.create(
        nac_economic_budget_code="RESOURCE",
        programme_budget_type=del_type,
        forecast_expenditure_type_name='Programme',
        forecast_expenditure_type_description='Programme Resource',
        forecast_expenditure_type_display_order=2
    ).save()

    ForecastExpenditureType.objects.create(
        nac_economic_budget_code="RESOURCE",
        programme_budget_type=ame_type,
        forecast_expenditure_type_name='Programme',
        forecast_expenditure_type_description='Programme Resource',
        forecast_expenditure_type_display_order=2
    ).save()

    ForecastExpenditureType.objects.create(
        nac_economic_budget_code="RESOURCE",
        programme_budget_type=admin_type,
        forecast_expenditure_type_name='Admin',
        forecast_expenditure_type_description='Admin Resource',
        forecast_expenditure_type_display_order=1
    ).save()


class Migration(migrations.Migration):
    dependencies = [("forecast", "0001_initial")]

    operations = [
        migrations.RunPython(populate_period),
        migrations.RunPython(create_forecast_expenditure_types),
    ]
