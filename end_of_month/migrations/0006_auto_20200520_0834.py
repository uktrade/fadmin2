# Generated by Django 2.2.10 on 2020-05-20 08:34

from django.db import migrations

def generate_drop_query(archived_period_name):
    return f"DROP VIEW if exists budget_forecast_{archived_period_name}_view CASCADE;"


def generate_create_query(archived_period_name, archived_period_id):
    drop_query = generate_drop_query(archived_period_name)
    query = f'Create view budget_forecast_{archived_period_name}_view as '\
        f'SELECT ROW_NUMBER () ' \
            f'OVER (ORDER BY coalesce(b.financial_code_id, f.financial_code_id)) as id,' \
            f'coalesce(b.financial_code_id, f.financial_code_id) as financial_code_id,' \
            f'coalesce(b.financial_year_id, f.financial_year_id) as financial_year, ' \
            f'coalesce(f.archived_period_id, b.archived_period_id) as archived_period_id, ' \
            f'coalesce(amount, 0) as budget, ' \
            f'coalesce(apr, 0) as apr, ' \
            f'coalesce(may, 0) as may, ' \
            f'coalesce(jun, 0) as jun, ' \
            f'coalesce(jul, 0) as jul, ' \
            f'coalesce(aug, 0) as aug, ' \
            f'coalesce(sep, 0) as sep, ' \
            f'coalesce(oct, 0) as oct, ' \
            f'coalesce(nov, 0) as nov, ' \
            f'coalesce("dec", 0) as "dec", ' \
            f'coalesce(jan, 0) as jan, ' \
            f'coalesce(feb, 0) as feb, ' \
            f'coalesce(mar, 0) as mar, ' \
            f'coalesce(adj1, 0) as adj1, ' \
            f'coalesce(adj2, 0) as adj2, ' \
            f'coalesce(adj3, 0) as adj3 ' \
            f'FROM monthly_forecast_{archived_period_name}  f ' \
            f'FULL OUTER JOIN public.end_of_month_monthlytotalbudget b ' \
            f'on b.financial_code_id = f.financial_code_id ' \
            f'and b.financial_year_id = f.financial_year_id ' \
            f'and b.archived_period_id = f.archived_period_id ' \
            f'WHERE coalesce(f.archived_period_id, b.archived_period_id) = {archived_period_id};'
    return f'{drop_query} {query}'


class Migration(migrations.Migration):

    dependencies = [
        ('end_of_month', '0005_create_month_views'),
    ]

    operations = [
        migrations.RunSQL(generate_create_query('apr', 1), generate_drop_query('apr')),
        migrations.RunSQL(generate_create_query('may', 2), generate_drop_query('may')),
        migrations.RunSQL(generate_create_query('jun', 3), generate_drop_query('jun')),
        migrations.RunSQL(generate_create_query('jul', 4), generate_drop_query('jul')),
        migrations.RunSQL(generate_create_query('aug', 5), generate_drop_query('aug')),
        migrations.RunSQL(generate_create_query('sep', 6), generate_drop_query('sep')),
        migrations.RunSQL(generate_create_query('oct', 7), generate_drop_query('oct')),
        migrations.RunSQL(generate_create_query('nov', 8), generate_drop_query('nov')),
        migrations.RunSQL(generate_create_query('dec', 9), generate_drop_query('dec')),
        migrations.RunSQL(generate_create_query('jan', 10), generate_drop_query('jan')),
        migrations.RunSQL(generate_create_query('feb', 11), generate_drop_query('feb')),
        migrations.RunSQL(generate_create_query('mar', 12), generate_drop_query('mar')),
        migrations.RunSQL(generate_create_query('adj1', 13), generate_drop_query('adj1')),
        migrations.RunSQL(generate_create_query('adj2', 14), generate_drop_query('adj2')),
        migrations.RunSQL(generate_create_query('adj3', 15), generate_drop_query('adj3')),
    ]
