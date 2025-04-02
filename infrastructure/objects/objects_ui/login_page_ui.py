from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from infrastructure.infra.dal.data_reposetory.data_rep import DataRep
from infrastructure.infra.dal.web_driver_extension.web_driver_extension import DriverEX
from infrastructure.objects.objects_ui.dashboard_page_ui import DashboardPageUi


class LoginPageUi:
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver

        # locators
        self.__user_dropdown_select = (By.ID, "userSelect")

    def select_user_filter(self, filter_value: str):
        select_element = DriverEX.search_element(self.__driver, self.__user_dropdown_select)
        Select(select_element).select_by_visible_text(filter_value)
        return self

    def click_on_login_btn(self)-> DashboardPageUi:
        DriverEX.force_click(self.__driver, by= DataRep.submit_transaction_btn)
        return DashboardPageUi(self.__driver)