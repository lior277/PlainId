import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(autouse=True)
def chrome_web_driver_base(request):
    options = webdriver.ChromeOptions()
    downloaded_binary_path = ChromeDriverManager().install()
    service = Service(executable_path=downloaded_binary_path)
    chrome_driver = webdriver.Chrome(
        service=service, options=options
    )
    chrome_driver.delete_all_cookies()
    chrome_driver.maximize_window()
    yield chrome_driver
    chrome_driver.close()
