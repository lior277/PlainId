from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from infrastructure.infra.dal.web_driver_extension.web_driver_extension import DriverEX
from infrastructure.objects.objects_ui.login_page_ui import LoginPageUi


class HomePageUi:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    # locators
        self.__customer_login_btn = By.CSS_SELECTOR, "button[ng-click='customer()']"

    def click_on_customer_login(self) -> LoginPageUi:
            DriverEX.force_click(driver=self.driver, by=self.__customer_login_btn)

            return LoginPageUi(self.driver)


