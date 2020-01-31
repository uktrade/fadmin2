# Generated by Django 2.2.8 on 2020-01-03 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0037_auto_20200102_0716'),
    ]

    operations = [
        migrations.RunSQL(
            """
                    DROP VIEW  if exists "forecast_oscarreturn";
                    CREATE VIEW "forecast_oscarreturn" as 
                    SELECT ROW_NUMBER () OVER (ORDER BY "treasurySS_subsegment"."sub_segment_code"),
                    coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id")
                    account_l5_code,
                    "treasurySS_subsegment"."sub_segment_code" ,
                    "treasurySS_subsegment"."sub_segment_long_name" ,
                    
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Apr' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "apr",
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Aug' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "aug",
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Dec' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "dec",
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Feb' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "feb",
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Jan' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "jan",
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Jul' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "jul",
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Jun' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "jun",
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Mar' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "mar",
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'May' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "may",
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Nov' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "nov",
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Oct' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "oct",
                    coalesce(round(SUM(CASE WHEN "forecast_financialperiod"."period_short_name" = 'Sep' THEN "forecast_monthlyfigureamount"."amount" ELSE NULL END)/100000), 0)  AS "sep"

                    FROM "forecast_monthlyfigureamount"
                        INNER JOIN
                         "forecast_monthlyfigure" on (forecast_monthlyfigureamount.monthly_figure_id = forecast_monthlyfigure.id)
                        INNER JOIN "forecast_financialcode" on (forecast_monthlyfigure.financial_code_id = forecast_financialcode.id)
                    LEFT OUTER JOIN "chartofaccountDIT_naturalcode"
                    ON ("forecast_financialcode"."natural_account_code_id" = "chartofaccountDIT_naturalcode"."natural_account_code")
                    INNER JOIN "costcentre_costcentre"
                    ON ("forecast_financialcode"."cost_centre_id" = "costcentre_costcentre"."cost_centre_code")
                    INNER JOIN "costcentre_directorate"
                    ON ("costcentre_costcentre"."directorate_id" = "costcentre_directorate"."directorate_code")
                    INNER JOIN "costcentre_departmentalgroup"
                    ON ("costcentre_directorate"."group_id" = "costcentre_departmentalgroup"."group_code")
                    INNER JOIN "chartofaccountDIT_programmecode" ON ("forecast_financialcode"."programme_id" = "chartofaccountDIT_programmecode"."programme_code")
                        INNER JOIN "forecast_financialperiod" ON ("forecast_monthlyfigure"."financial_period_id" = "forecast_financialperiod"."financial_period_code")
                    LEFT OUTER JOIN "treasurySS_subsegment" ON ("costcentre_departmentalgroup"."treasury_segment_fk_id" = "treasurySS_subsegment"."Segment_code_id"
                    AND "chartofaccountDIT_programmecode"."budget_type_fk_id" = "treasurySS_subsegment"."dit_budget_type_id")
                    INNER JOIN "core_financialyear" ON ("forecast_monthlyfigure"."financial_year_id" = "core_financialyear"."financial_year")
                    WHERE "core_financialyear"."current" = TRUE and forecast_monthlyfigureamount.version = 1
                    GROUP BY coalesce("chartofaccountDIT_naturalcode"."account_L5_code_upload_id", "chartofaccountDIT_naturalcode"."account_L5_code_id"),
                    "treasurySS_subsegment"."sub_segment_code" ;        

        """,
            'DROP VIEW "forecast_oscarreturn";',
        )
    ]