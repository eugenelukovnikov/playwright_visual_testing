import pytest


def test_homepage(screenshot_helper, page):
    page.goto("https://klinika-innomed.ru/")
    screenshot_helper.take_and_compare("homepage")
