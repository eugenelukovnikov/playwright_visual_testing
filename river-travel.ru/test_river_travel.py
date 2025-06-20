import pytest

def test_homepage(screenshot_helper, page, scrolled_page):
    
    scrolled_page("https://river-travel.ru")

    widgets = page.query_selector_all(
        "//div[@id='modal-cookie'] | //jdiv[1]"
    )

    for widget in widgets:
        widget.evaluate("el => el.remove()")


    screenshot_helper.take_and_compare("homepage")
