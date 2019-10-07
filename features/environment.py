from behave import use_fixture
from core.behave_fixtures import django_test_runner, django_test_case
import os
from selenium import webdriver
from browserstack.local import Local
from django.conf import settings
import os, json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"


def before_all(context):
    use_fixture(django_test_runner, context)


def before_scenario(context, scenario):
    use_fixture(django_test_case, context)

TASK_ID = int(os.environ['TASK_ID']) if 'TASK_ID' in os.environ else 0

CONFIG = {
  "server": "hub.browserstack.com",
  "user": "uktitools1",
  "key": "rJFxac2sLtJvBn5hUdMK",

  "capabilities": {
    "browserstack.local": True,
    "name": "Bstack-[Behave] Local Test"
  },

  "environments": [{
    "browser": "chrome"
  }]
}

bs_local = None

BROWSERSTACK_USERNAME = settings.BROWSERSTACK_USERNAME
BROWSERSTACK_ACCESS_KEY = settings.BROWSERSTACK_ACCESS_KEY


def start_local():
    """Code to start browserstack local before start of test."""
    global bs_local
    bs_local = Local()
    bs_local_args = { "key": BROWSERSTACK_ACCESS_KEY, "forcelocal": "true" }
    bs_local.start(**bs_local_args)


def stop_local():
    """Code to stop browserstack local after end of test."""
    global bs_local
    if bs_local is not None:
        bs_local.stop()


def before_feature(context, feature):
    # desired_capabilities = CONFIG['environments'][TASK_ID]
    #
    # for key in CONFIG["capabilities"]:
    #     if key not in desired_capabilities:
    #         desired_capabilities[key] = CONFIG["capabilities"][key]
    #
    # if 'BROWSERSTACK_APP_ID' in os.environ:
    #     desired_capabilities['app'] = os.environ['BROWSERSTACK_APP_ID']
    #
    # if "browserstack.local" in desired_capabilities and desired_capabilities["browserstack.local"]:
    #     start_local()
    #
    # context.browser = webdriver.Remote(
    #     desired_capabilities=desired_capabilities,
    #     command_executor="http://%s:%s@%s/wd/hub" % (BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, CONFIG['server'])
    # )

    context.browser = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.FIREFOX
    )
    context.browser.implicitly_wait(5)



    # self.firefox = webdriver.Remote(
    #     command_executor='http://selenium_hub:4444/wd/hub',
    #     desired_capabilities=DesiredCapabilities.FIREFOX
    # )
    # self.firefox.implicitly_wait(10)


def after_feature(context, feature):
    context.browser.quit()
    # stop_local()