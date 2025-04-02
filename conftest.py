import pytest

from infrastructure.infra.dal.data_reposetory.data_rep import DataRep
from tests.test_suit_Base import TestSuitBase


@pytest.fixture(scope='function')
def setup_and_teardown():
    # Setup code here (run before each test)
    print("Setup: This will run before each test")
    driver = TestSuitBase.get_driver()
    driver.maximize_window()
    driver.get(DataRep.banking_project_url)

    yield driver  # Provide the driver to the test

    # Teardown code here (run after each test)
    print("Teardown: This will run after each test")
    if driver:
        TestSuitBase.driver_dispose(driver=driver)