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
        "Добавьте их в .env или в переменные окружения."
    )

# Первая статья в ленте на экране Home.
# Вместо абсолютного XPath (.../XCUIElementTypeCell[30]/...), который
# скопирован из инспектора и ломается при любом изменении иерархии,
# берём первую ячейку таблицы.
FIRST_ARTICLE = (
    AppiumBy.XPATH,
    "(//XCUIElementTypeTable//XCUIElementTypeCell)[1]",
)

# Заголовок статьи внутри ячейки (первый StaticText ячейки)
FIRST_ARTICLE_TITLE = (
    AppiumBy.XPATH,
    "(//XCUIElementTypeTable//XCUIElementTypeCell)[1]"
    "//XCUIElementTypeStaticText[1]",
)

# Экран статьи (встроенный браузер)
ARTICLE_WEBVIEW = (AppiumBy.CLASS_NAME, "XCUIElementTypeWebView")


def test_open_article():
    options = XCUITestOptions()

    options.set_capability("browserstack.user", USER)
    options.set_capability("browserstack.key", KEY)
    options.set_capability("app", "bs://sample.app")  # <- подставьте URL вашего приложения

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
        # 1. Ждём, пока загрузится лента, и находим первую статью
        article = wait.until(EC.element_to_be_clickable(FIRST_ARTICLE))

        # Запоминаем заголовок и исходный экран
        title = wait.until(
            EC.presence_of_element_located(FIRST_ARTICLE_TITLE)
        ).text
        previous_page = driver.page_source

        # 2. Тапаем по статье
        article.click()

        # 3. Статья должна открыться в WebView
        wait.until(EC.presence_of_element_located(ARTICLE_WEBVIEW))

        # 4. Экран изменился, а лента (Home) больше не на переднем плане
        assert driver.page_source != previous_page, (
            f"После нажатия на статью «{title}» экран не изменился"
        )
    finally:
        driver.quit()
