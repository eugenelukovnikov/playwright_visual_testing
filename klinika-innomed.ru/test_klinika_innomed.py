import pytest


def test_homepage(screenshot_helper, page):
    page.goto("https://klinika-innomed.ru/", wait_until="networkidle")
    screenshot_helper.take_and_compare("homepage")
