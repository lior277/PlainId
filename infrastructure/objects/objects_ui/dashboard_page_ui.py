from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from infrastructure.infra.dal.data_reposetory.data_rep import DataRep
from infrastructure.infra.dal.web_driver_extension.web_driver_extension import DriverEX
from infrastructure.objects.objects_ui.transactions_page_ui import TransactionsPageUi


class DashboardPageUi:
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver

        # locators
        self.__deposit_btn = By.CSS_SELECTOR, "button[ng-click='deposit()']"
        self.__withdrawal_btn = By.CSS_SELECTOR, "button[ng-click='withdrawl()']"
        self.__amount_input = By.CSS_SELECTOR, "input[ng-model='amount']"

    def click_on_transactions(self) -> TransactionsPageUi:
        DriverEX.force_click(driver=self.__driver, by=DataRep.transactions_btn)

        return TransactionsPageUi(self.__driver)

    def click_on_deposit(self) -> 'DashboardPageUi':
        DriverEX.force_click(driver=self.__driver, by=self.__deposit_btn)

        return self

    def click_on_withdrawal(self) -> 'DashboardPageUi':
        DriverEX.force_click(driver=self.__driver, by=self.__withdrawal_btn)

        return self

    def set_amount(self, amount: str) -> 'DashboardPageUi':
        DriverEX.send_keys_auto(driver=self.__driver, by=self.__amount_input, input_text=amount)

        return self

    def click_on_submit_transaction(self) -> 'DashboardPageUi':
        DriverEX.force_click(driver= self.__driver, by= DataRep.submit_transaction_btn)
        return self
