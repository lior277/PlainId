from datetime import datetime

from infrastructure.enums.transaction_types import TransactionTypes
from infrastructure.infra.dal.data_reposetory.data_rep import DataRep
from infrastructure.infra.utils.assert_utils import CustomAssert
from infrastructure.objects.objects_ui.home_page_ui import HomePageUi
from tests.test_suit_Base import TestSuitBase


class TestVerifyBalanceWhenDepositAndWithdraw(TestSuitBase):
    @classmethod
    def setup_class(cls):
        # This runs once for the class
        cls.driver = cls.get_driver()
        cls.driver.maximize_window()
        cls.driver.get(DataRep.banking_project_url)
        cls.expected_deposit_amount = "200"
        cls.expected_withdrawal_amount = "100"
        cls.expected_date = datetime.now().strftime("%b %d, %Y").replace(" 0", " ")

        # Initialize page objects
        cls.home_page_ui = HomePageUi(cls.driver)

        # Login
        cls.dashboard_page_ui = cls.home_page_ui \
            .click_on_customer_login() \
            .select_user_filter(DataRep.login_user_name) \
            .click_on_login_btn()

        # reset transactions
        cls.dashboard_page_ui\
            .click_on_transactions()\
            .click_on_reset()\
            .click_on_back()

    @classmethod
    def teardown_class(cls):
        if cls.driver:
            cls.driver_dispose(driver=cls.driver)

    def test_verify_balance_when_deposit_and_withdraw(self):

        # create Deposit
        self.dashboard_page_ui \
            .click_on_deposit() \
            .set_amount(self.expected_deposit_amount) \
            .click_on_submit_transaction()

        # create withdrawal
        self.dashboard_page_ui \
            .click_on_withdrawal() \
            .set_amount(self.expected_withdrawal_amount) \
            .click_on_submit_transaction()

        # transactions
        transactions_data = self.dashboard_page_ui \
            .click_on_transactions() \
            .get_transactions_data()

        actual_deposit_data = transactions_data[TransactionTypes.CREDIT.name][0]
        actual_withdrawal_data = transactions_data[TransactionTypes.DEBIT.name][0]

        CustomAssert.assert_multiple([
            lambda: CustomAssert.assert_in(
                self.expected_date,
                actual_deposit_data.date_time,
                f"Expected deposit date: {self.expected_date}, " +
                f"Actual deposit date: {actual_deposit_data.date_time}"
            ),
            lambda: CustomAssert.assert_true(
                self.expected_deposit_amount == actual_deposit_data.amount,
                f"Expected deposit amount: {self.expected_deposit_amount}, " +
                f"Actual deposit amount: {actual_deposit_data.amount}"
            ),
            lambda: CustomAssert.assert_true(
                TransactionTypes.CREDIT.value == actual_deposit_data.transaction_type,
                " Expected deposit transaction type: Credit, " +
                f" Actual deposit transaction type: {actual_deposit_data.transaction_type}"
            ),
            lambda: CustomAssert.assert_in(
                self.expected_date,
                actual_withdrawal_data.date_time,
                f" Expected withdrawal date: {self.expected_date}, " +
                f" Actual withdrawal date: {actual_withdrawal_data.date_time}"
            ),
            lambda: CustomAssert.assert_true(
                self.expected_withdrawal_amount == actual_withdrawal_data.amount,
                f" Expected withdrawal amount: {self.expected_withdrawal_amount}, " +
                f" Actual withdrawal amount: {actual_withdrawal_data.amount}"
            ),
            lambda: CustomAssert.assert_true(
                TransactionTypes.DEBIT.value == actual_withdrawal_data.transaction_type,
                " Expected withdrawal transaction type: Debit, " +
                f" Actual withdrawal transaction type: {actual_withdrawal_data.transaction_type}"
            )
        ])
