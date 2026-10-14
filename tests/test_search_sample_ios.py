import os
import time

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
        "Добавьте их в .env или в переменные окружения."
    )


def test_open_article():
    options = XCUITestOptions()

    # Set your access credentials
    options.set_capability("browserstack.user", USER)
    options.set_capability("browserstack.key", KEY)

    # Set URL of the application under test
    options.set_capability("app", "bs://sample.app")

    # Specify device and os_version for testing
    options.set_capability("platformName", "ios")
    options.set_capability("deviceName", "iPhone 14 Pro Max")
    options.set_capability("platformVersion", "16.0")

    # Set other BrowserStack capabilities
    options.set_capability("project", "First Python Project")
    options.set_capability("build", "browserstack-build-1")
    options.set_capability("name", "open_article_ios")

    driver = webdriver.Remote(
        f"https://{USER}:{KEY}@hub.browserstack.com/wd/hub",
        options=options,
    )

    try:
        # Открываем первую статью в ленте
        first_article = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (AppiumBy.XPATH, "(//XCUIElementTypeTable//XCUIElementTypeCell)[1]")
            )
        )
        first_article.click()

        # Ждём, пока статья откроется во встроенном браузере (webview)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (AppiumBy.CLASS_NAME, "XCUIElementTypeWebView")
            )
        )
        time.sleep(5)

        # Проверяем, что на странице есть контент
        all_texts = driver.find_elements(
            AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText"
        )
        assert len(all_texts) > 0
    finally:
        driver.quit()