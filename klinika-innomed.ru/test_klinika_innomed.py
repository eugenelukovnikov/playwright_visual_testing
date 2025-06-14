import pytest

def test_homepage(screenshot_helper, page, scrolled_page):

    scrolled_page("https://klinika-innomed.ru/")  # Загрузка + прокрутка вниз
    
    widgets = page.query_selector_all(
        "//div[@class='medflex-round-widget'] | //div[contains(@class,'b24-widget-button-wrapper')]"
    )

    for widget in widgets:
        widget.evaluate("el => el.remove()")

    screenshot_helper.take_and_compare("homepage")
