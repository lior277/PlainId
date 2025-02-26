from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By

from infrastructure.Infra.dal.web_driver_extension.web_driver_extension import DriverEX
from infrastructure.objects.objects_ui.careers_page_ui import CareersPageUi


class HomePageUi:
    def __init__(self, driver: webdriver) -> None:
        self.driver = driver

    # locators
        self.__career_link = By.CSS_SELECTOR, "a[href='/careers/']"

    def click_on_careers_link(self) -> CareersPageUi:
            DriverEX.force_click(driver=self.driver, by=self.__career_link)
            return CareersPageUi(self.driver)


