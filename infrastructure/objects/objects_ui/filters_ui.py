
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from infrastructure.Infra.dal.web_driver_extension.web_driver_extension import DriverEX


class FiltersUi:
    def __init__(self, driver: webdriver) -> None:
        self.__driver = driver

        # locators
        self.__department_filter_select_ext = By.CSS_SELECTOR, "select[id='department-filter']"

    def select_department_filter(self, filter_value: str) -> None:
        DriverEX.select_element_from_dropdown_by_value(self.__driver, self.__department_filter_select_ext, filter_value)
        return self