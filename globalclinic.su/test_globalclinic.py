import pytest

def test_homepage(screenshot_helper, page, scrolled_page):

    scrolled_page("https://globalclinic.su/")  # Загрузка + прокрутка вниз
    
    widgets = page.query_selector_all(
        "//div[@class='medflex-round-widget'] | //section[contains(@class, 'r52-a-cookies')]"
    )

    for widget in widgets:
        widget.evaluate("el => el.remove()")

    screenshot_helper.take_and_compare("homepage")
