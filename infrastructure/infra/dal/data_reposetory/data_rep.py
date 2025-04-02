from selenium.webdriver.common.by import By


class DataRep:
    banking_project_url = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"
    submit_transaction_btn = By.CSS_SELECTOR, "button[type='submit']"
    transactions_btn = By.CSS_SELECTOR, "button[ng-click='transactions()']"
    time_to_wait_from_seconds  = 30
    login_user_name = "Harry Potter"
