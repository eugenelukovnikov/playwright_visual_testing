import pytest


def test_homepage(screenshot_helper, page, scrolled_page):

    widgets_selectors = [
        "//div[@id='modal-cookie']",
        "//jdiv[1]"
    ]

    scrolled_page("https://river-travel.ru", widgets_delete=widgets_selectors)

    screenshot_helper.take_and_compare("homepage")
