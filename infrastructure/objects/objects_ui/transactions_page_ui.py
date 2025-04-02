from time import sleep
from typing import List, Dict

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from infrastructure.enums.transaction_types import TransactionTypes
from infrastructure.infra.dal.data_reposetory.data_rep import DataRep
from infrastructure.infra.dal.web_driver_extension.web_driver_extension import DriverEX
from infrastructure.objects.data_classes.transactions import Transactions


class TransactionsPageUi:
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver

        # locators
        self.__back_btn = By.CSS_SELECTOR, "button[ng-click='back()']"
        self.__reset_btn = (By.CSS_SELECTOR, "button[ng-click='reset()']")
        self.__transactions_data = (By.CSS_SELECTOR, "table[class*='table'] tbody tr")

    def click_on_back(self) -> 'TransactionsPageUi':
        DriverEX.force_click(driver=self.__driver, by=self.__back_btn)

        return self

    def click_on_reset(self) -> 'TransactionsPageUi':
        elements = DriverEX.search_elements(driver=self.__driver, by=self.__transactions_data, wait_if_empty=False)

        if len(elements) > 0:
            DriverEX.force_click(driver=self.__driver, by=self.__reset_btn)

        return self

    def wait_for_transactions_data(self) -> 'TransactionsPageUi':
        max_attempts = 5

        for _ in range(max_attempts):
            elements = DriverEX.search_elements(driver=self.__driver, by=self.__transactions_data, wait_if_empty=False)

            if len(elements) > 0:
                return self

            DriverEX.force_click(driver=self.__driver, by=self.__back_btn)
            sleep(0.3)
            DriverEX.force_click(driver=self.__driver, by=DataRep.transactions_btn)
        return self

    def get_transactions_data(self) -> Dict[str, List[Transactions]]:
        self.wait_for_transactions_data()
        elements = DriverEX.search_elements(driver=self.__driver, by=self.__transactions_data)

        # Initialize the dictionary with predefined keys
        transaction_dict: Dict[str, List[Transactions]] = {
            TransactionTypes.CREDIT.name: [],  # For deposits
            TransactionTypes.DEBIT.name: []  # For withdrawals
        }

        for element in elements:
            columns = element.find_elements(By.TAG_NAME, "td")

            if len(columns) >= 3:
                date_time = columns[0].text.strip()
                amount = columns[1].text.strip()
                transaction_type = columns[2].text.strip()

                transaction = Transactions(
                    date_time=date_time,
                    amount=amount,
                    transaction_type=transaction_type
                )

                # Use .value instead of .name for comparison with UI text
                if transaction_type == TransactionTypes.CREDIT.value:
                    transaction_dict[TransactionTypes.CREDIT.name].append(transaction)
                elif transaction_type == TransactionTypes.DEBIT.value:
                    transaction_dict[TransactionTypes.DEBIT.name].append(transaction)

        return transaction_dict