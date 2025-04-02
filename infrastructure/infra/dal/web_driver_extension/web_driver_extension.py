from time import sleep
from typing import Any, List, Optional

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    ElementNotVisibleException,
    ElementNotSelectableException,
    InvalidSelectorException,
    NoSuchFrameException,
    WebDriverException,
    TimeoutException)

from infrastructure.infra.dal.data_reposetory.data_rep import DataRep


def ignore_exception_types():
    return [
        NoSuchElementException,
        ElementNotInteractableException,
        ElementNotVisibleException,
        ElementNotSelectableException,
        InvalidSelectorException,
        NoSuchFrameException,
        WebDriverException
    ]

class SearchElement:
    def __init__(self, by: tuple):
        self.by = by
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> Optional[WebElement]:
        try:
            element = driver.find_element(*self.by)
            if element is not None:
                if element.is_displayed() and element.is_enabled():
                    return element
            return None
        except StaleElementReferenceException:
            sleep(0.3)
            return None
        except Exception as e:
            self.last_exception = e
            return None


class SearchElements:
    def __init__(self, by: tuple):
        self.by = by
        self.last_exception = None
        # Add a flag to track if we've found elements, even if empty
        self.elements_found = False

    def __call__(self, driver: WebDriver) -> Optional[list[WebElement]]:
        try:
            elements = driver.find_elements(*self.by)
            # Mark that we've successfully found elements (even if empty list)
            self.elements_found = True
            # Return elements regardless of count
            return elements
        except StaleElementReferenceException:
            sleep(0.3)
            self.last_exception = Exception(f"StaleElementReferenceException when finding elements with locator: {self.by}")
            return None
        except Exception as e:
            self.last_exception = Exception(f"Error in SearchElements: {str(e)} for locator: {self.by}")
            return None

class ScrollToElement:
    def __init__(self, by: tuple):
        self.by = by
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> Any:
        try:
            element = driver.find_element(*self.by)
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            sleep(0.5)
            return element
        except Exception as e:
            self.last_exception = e
            return None


class ForceClick:
    def __init__(self, by: tuple, element: WebElement = None):
        self.by = by
        self.element = element
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> Optional[WebElement]:
        try:
            # Use the provided element if available, otherwise find it using the locator
            if self.element is not None:
                element = self.element
            else:
                element = driver.find_element(*self.by)

            if element.is_enabled():
                element.click()
            return element
        except StaleElementReferenceException:
            sleep(0.3)
            return None
        except ElementClickInterceptedException:
            ScrollToElement(self.by)(driver)
            return None
        except Exception as e:
            self.last_exception = e
            return None


class GetElementText:
    def __init__(self, by: tuple):
        self.by = by
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> str:
        try:
            element = driver.find_element(*self.by)
            text = element.get_attribute("innerText") or element.get_attribute("value") or ""
            return text.strip()
        except StaleElementReferenceException:
            sleep(0.3)
            return ""
        except Exception as e:
            self.last_exception = e
            return ""


class SendKeysAuto:
    def __init__(self, by: tuple, input_text: str):
        self.by = by
        self.input_text = input_text
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> bool:
        try:
            element = DriverEX.search_element(driver, self.by)
            existing_text = element.get_attribute("value") or element.text

            if self.input_text != existing_text:
                element.clear()
                element.send_keys(self.input_text)
                return False
            return True
        except StaleElementReferenceException:
            sleep(0.3)
            return False
        except Exception as e:
            self.last_exception = e
            return False


    @staticmethod
    def search_element(driver: WebDriver, by: tuple) -> WebElement:
        search = SearchElement(by)
        try:
            return WebDriverWait(driver, DataRep.time_to_wait_from_seconds,
                                 ignored_exceptions=ignore_exception_types())\
                .until(search)

        except TimeoutException:
            if search.last_exception:
                raise search.last_exception
            raise


    @staticmethod
    def send_keys_auto(driver: WebDriver, by: tuple, input_text: str) -> None:
        send_keys = SendKeysAuto(by, input_text)
        try:
            WebDriverWait(driver,
                          DataRep.time_to_wait_from_seconds,
                          ignored_exceptions=ignore_exception_types())\
                .until(send_keys)

        except TimeoutException:
            if send_keys.last_exception:
                raise send_keys.last_exception
            raise

    @staticmethod
    def search_elements(driver: WebDriver, by: tuple, wait_if_empty=False) -> List[WebElement]:
        search = SearchElements(by)

        if not wait_if_empty:
            # If we don't need to wait, just do a direct find_elements call
            return driver.find_elements(*by)

        try:
            elements = WebDriverWait(driver,
                                     DataRep.time_to_wait_from_seconds,
                                     ignored_exceptions=ignore_exception_types()) \
                .until(search)

            return elements if elements is not None else []

        except TimeoutException:
            # Check if we found elements but the wait timed out because the list was empty
            if search.elements_found:
                return []

            if search.last_exception:
                print(f"Detailed error when searching for elements: {str(search.last_exception)}")
                print(f"Current URL: {driver.current_url}")
                print(f"Page title: {driver.title}")

            # Return empty list for any type of timeout
            return []

    @staticmethod
    def force_click(driver: WebDriver, by: tuple, element: WebElement = None) -> bool:
        click = ForceClick(by, element)
        try:
            element = WebDriverWait(driver,
                                    DataRep.time_to_wait_from_seconds,
                                    ignored_exceptions=ignore_exception_types())\
                .until(click)

            return element is not None
        except TimeoutException:
            if click.last_exception:
                raise click.last_exception
            raise


    @staticmethod
    def get_element_text(driver: WebDriver, by: tuple) -> str:
        get_text = GetElementText(by)
        try:
            return WebDriverWait(driver,
                                 DataRep.time_to_wait_from_seconds,
                                 ignored_exceptions=ignore_exception_types())\
                .until(get_text)

        except TimeoutException:
            if get_text.last_exception:
                raise get_text.last_exception
            raise

