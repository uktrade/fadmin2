import django_tables2 as tables


class FadminTable(tables.Table):
    class Meta:
        template_name = "django_tables_2_bootstrap.html"
        attrs = {
            "class": "govuk-table",
            "thead": {"class": "govuk-table__head"},
            "tr": {"class": "govuk-table__row"},
            "th": {"class": "govuk-table__header"},
            "tbody": {"class": "govuk-table__body"},
            "td": {"class": "govuk-table__cell"},
            "tf": {"class": "govuk-table__cell"},
            "a": {"class": "govuk-link"},
        }
        empty_text = "There are no results matching your search criteria."
