import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

USER = os.getenv("BROWSERSTACK_USERNAME")
KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

if not USER or not KEY:
    raise RuntimeError(
        "Не заданы BROWSERSTACK_USERNAME / BROWSERSTACK_ACCESS_KEY. "
        "Добавьте их в .env или в переменные окружения."
    )

APP_ID = "org.wikipedia.alpha"
TIMEOUT = 30


def by_id(name: str) -> tuple:
    return AppiumBy.ID, f"{APP_ID}:id/{name}"


@pytest.fixture
def driver():
    options = UiAutomator2Options()
    options.set_capability("browserstack.user", USER)
    options.set_capability("browserstack.key", KEY)
    options.set_capability("app", "bs://0889eb57ee4bff445c6491d1a9833af99be7ca97")
    options.set_capability("platformName", "android")
    options.set_capability("deviceName", "Samsung Galaxy S22 Ultra")
    options.set_capability("platformVersion", "12.0")
    options.set_capability("project", "First Python Project")
    options.set_capability("build", "browserstack-build-1")
    options.set_capability("name", "open_article")

    drv = webdriver.Remote(
        f"https://{USER}:{KEY}@hub.browserstack.com/wd/hub",
        options=options,
    )
    yield drv
    drv.quit()  # сессия закроется даже если тест упал


def wait_clickable(driver, locator):
    return WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable(locator))


def wait_present(driver, locator):
    return WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located(locator))


def search_for(driver, query: str):
    """Пропускает онбординг и вводит поисковый запрос."""
    # skip onboarding screen (back)
    wait_clickable(driver, (AppiumBy.ACCESSIBILITY_ID, "Wikipedia"))
    driver.back()

    wait_clickable(driver, by_id("nav_tab_search")).click()
    wait_clickable(driver, (AppiumBy.ACCESSIBILITY_ID, "Close")).click()
    wait_clickable(driver, by_id("search_text_view")).click()
    wait_clickable(driver, by_id("search_src_text")).send_keys(query)


def test_open_article(driver):
    search_for(driver, "Appium")

    results_container = wait_present(driver, by_id("fragment_search_results"))

    # ждём результаты: TextView внутри контейнера, в тексте которых есть запрос
    results = WebDriverWait(driver, TIMEOUT).until(
        lambda d: [
            t
            for t in results_container.find_elements(
                AppiumBy.CLASS_NAME, "android.widget.TextView"
            )
            if "Appium" in (t.text or "")
        ]
    )

    first_result = results[0]
    expected_title = first_result.text
    first_result.click()

    # статья открылась
    wait_present(driver, by_id("page_web_view"))

    # заголовок открытой статьи совпадает с выбранным результатом
    # (если в вашей версии приложения этого id нет - смотрите комментарий ниже)
    article_title = wait_present(driver, by_id("view_page_title_text"))
    assert expected_title in article_title.text
