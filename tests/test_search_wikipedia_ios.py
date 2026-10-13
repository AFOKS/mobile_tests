import os

from appium import webdriver
from appium.options.ios import XCUITestOptions
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
        "Добавьте их в .env или переменные окружения."
    )


def test_open_article():
    options = XCUITestOptions()

    options.set_capability("browserstack.user", USER)
    options.set_capability("browserstack.key", KEY)
    options.set_capability("app", "bs://sample.app")

    options.set_capability("platformName", "iOS")
    options.set_capability("deviceName", "iPhone 14 Pro Max")
    options.set_capability("platformVersion", "16.0")

    options.set_capability("project", "BrowserStack Sample")
    options.set_capability("build", "browserstack-build-1")
    options.set_capability("name", "open_article_ios")

    driver = webdriver.Remote(
        f"https://{USER}:{KEY}@hub.browserstack.com/wd/hub",
        options=options,
    )

    wait = WebDriverWait(driver, 30)

    try:
        # Находим статью по XPath
        article = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "/XCUIElementTypeApplication/XCUIElementTypeWindow/"
                    "XCUIElementTypeOther[2]/XCUIElementTypeOther/"
                    "XCUIElementTypeOther/XCUIElementTypeOther/"
                    "XCUIElementTypeOther/XCUIElementTypeOther/"
                    "XCUIElementTypeOther/XCUIElementTypeOther/"
                    "XCUIElementTypeTable/XCUIElementTypeCell[30]/"
                    "XCUIElementTypeOther[1]/XCUIElementTypeOther",
                )
            )
        )

        # Запоминаем исходный экран
        previous_page = driver.page_source

        # Тапаем по статье
        article.click()

        # Ждём перехода на экран статьи
        wait.until(lambda d: d.page_source != previous_page)

        # Проверяем, что экран изменился
        assert driver.page_source != previous_page, (
            "После нажатия на статью экран не изменился"
        )

    finally:
        driver.quit()