from selenium import webdriver
import pytest

@pytest.fixture(params=["chrome", "edge", "firefox"], scope='class')
def setup(request):
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        browser = webdriver.Chrome(options=options)
        return browser
    elif request.param == "edge":
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        browser = webdriver.Edge(options=options)
        return browser
    elif request.param == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        browser = webdriver.Firefox(options=options)
        return browser


