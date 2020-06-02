# from behave import (
#     given,
#     when,
#     then,
# )
#
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as ec
#
# from features.environment import (
#     create_test_user,
# )
#
#
# @given(u'the user selects Other from the Company Received field')
# def step_impl(context):
#
#     create_test_user(context)
#
#     context.browser.get(
#         f'{context.base_url}/gifthospitality/receive'
#     )
#
#
# @when(u'the user selects Other')
# def step_impl(context):
#
#     WebDriverWait(context.browser, 500).until(
#         ec.presence_of_element_located((By.ID, "id_company"))
#     )
#
#
# @then(u'a free text field for Other appears')
# def step_impl(context):
#     company_field = context.browser.find_element_by_id(
#         'id_company'
#     )
#
#     options_list = company_field.find_element_by_xpath("//option[@text='Other']").click()
#     # options_real_list = company_field.find_element_by_value(22)
#     # options_real_list.click()
#     # options_real_list.save()
#     print (options_list)
#     for other_company in company_field.find_elements_by_tag("option"):
#         print(other_company.text)
#         if other_company.id == 'Other':
#             other_company.click()
#             break
#         else:
#             print("cant find")
#
#     # WebDriverWait(context.browser, 500).until(
#     #     ec.presence_of_element_located((By.CSS_SELECTOR, ))
#     # )
#
#     other_company_field = context.browser.find_element_by_id('id_company_name')
#     parent = other_company_field.find_element_by_xpath('..')
#     print(parent)
#     import time
#     print(parent.get_attribute('style'))
#     print("goodbye")
#
#     assert parent.get_attribute("style") == 'display: none;'
#
#     # assert other_company_field.is_displayed() == True
#
#     # assert 1==2
