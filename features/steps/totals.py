from behave import (
    then,
)


@then(u'the totals are updated')
def step_impl(context):
    year_to_date = context.browser.find_element_by_id(
        "year-to-date"
    ).get_attribute(
        'innerHTML'
    )

    year_total = context.browser.find_element_by_id(
        "year-total"
    ).get_attribute(
        'innerHTML'
    )

    sept_total = context.browser.find_element_by_id(
        "total_6"
    ).get_attribute(
        'innerHTML'
    )

    assert year_to_date == "0"
    assert year_total == "10,000"
    assert sept_total == "10,000"
