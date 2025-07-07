import pytest


def test_homepage(screenshot_helper, page, scrolled_page):

    slider = """
        document.querySelectorAll('.owl-carousel').forEach(el => {
            $(el).trigger('stop.owl.autoplay');
        });
        """

    widgets_selectors = [
        "//div[@class='medflex-round-widget']",
        "//div[contains(@class,'b24-widget-button-wrapper')]"
    ]

    # Загрузка + прокрутка вниз + удаление виджетов и остановка слайдера
    scrolled_page("https://klinika-innomed.ru/",
                  slider_stop=slider, widgets_delete=widgets_selectors)

    screenshot_helper.take_and_compare("homepage")
