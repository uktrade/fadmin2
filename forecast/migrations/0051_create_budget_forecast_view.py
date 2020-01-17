# Generated by Django 2.2.8 on 2020-01-16 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0050_auto_20200116_1204'),
    ]

    operations = [

        migrations.RunSQL(

            """DROP VIEW if exists
                    forecast_forecast_budget_view ;
                    
                    CREATE VIEW
                    forecast_forecast_budget_view 
                    as
                    SELECT row_number() OVER () as id, forecast_forecastmonthlyfigure.financial_code_id, "forecast_forecastmonthlyfigure"."financial_year_id" as financial_year,
                    COALESCE (SUM("forecast_budgetmonthlyfigure"."amount"),0) AS "budget",
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 1 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "apr", 
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 2 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "may", 
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 3 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "jun", 
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 4 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "jul", 
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 5 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "aug", 
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 6 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "sep", 
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 7 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "oct", 
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 8 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "nov", 
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 9 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "dec", 
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 10 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "jan", 
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 11 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "feb", 
                           COALESCE(SUM(CASE WHEN "forecast_financialperiod"."financial_period_code" = 12 THEN "forecast_forecastmonthlyfigure"."amount" ELSE NULL END), 0) AS "mar" 
                    FROM "forecast_forecastmonthlyfigure"
                        INNER JOIN "forecast_financialperiod" ON ("forecast_forecastmonthlyfigure"."financial_period_id" = "forecast_financialperiod"."financial_period_code")
                        LEFT OUTER  JOIN forecast_budgetmonthlyfigure ON 
                        forecast_forecastmonthlyfigure.financial_code_id = "forecast_budgetmonthlyfigure"."financial_code_id"
                        AND forecast_forecastmonthlyfigure.financial_year_id = "forecast_budgetmonthlyfigure"."financial_year_id"
                    GROUP BY forecast_forecastmonthlyfigure.financial_code_id, "forecast_forecastmonthlyfigure"."financial_year_id"                   
        """,
        'DROP VIEW "forecast_forecast_budget_view";',

    )

    ]
