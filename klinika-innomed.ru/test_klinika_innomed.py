import pytest


def test_homepage(screenshot_helper, page):
    page.goto("https://klinika-innomed.ru/", wait_until="load")

    prev_height = 0
    max_scrolls = 20
    scrolls = 0

    while scrolls < max_scrolls:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        page.wait_for_timeout(1000)  # ждем 2 секунды для подгрузки контента
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == prev_height:
            break  # достигли конца страницы, новых данных нет
        prev_height = new_height
        scrolls += 1

    screenshot_helper.take_and_compare("homepage")
