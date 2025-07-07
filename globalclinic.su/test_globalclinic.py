import pytest

def test_homepage(screenshot_helper, page, scrolled_page):

    slider = """
        const swipers = document.querySelectorAll('.swiper.hero-slider');
        swipers.forEach(el => {
            const swiperInstance = el.swiper;
            if (swiperInstance && swiperInstance.autoplay) {
                swiperInstance.autoplay.stop();
            }
        });
    """

    widgets_selectors=[
            "//div[@class='medflex-round-widget']",
            "//section[contains(@class, 'r52-a-cookies')]"
        ]

    scrolled_page("https://globalclinic.su/", slider_stop=slider, widgets_delete = widgets_selectors)


    screenshot_helper.take_and_compare("homepage")
