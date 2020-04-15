# TODO - Test that the index page actually renders

from bs4 import BeautifulSoup


from django.test import (
    TestCase,
)
from django.urls import reverse

from core.test.test_base import RequestFactoryBase