import pytest

def test_homepage(screenshot_helper, page):
    page.goto("https://river-travel.ru")
    screenshot_helper.take_and_compare("homepage")