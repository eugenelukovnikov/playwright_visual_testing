import pytest


def test_homepage(screenshot_helper, page):
    page.goto("https://klinika-innomed.ru/", wait_until="networkidle")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    screenshot_helper.take_and_compare("homepage")
