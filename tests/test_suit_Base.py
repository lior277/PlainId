from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging


class TestSuitBase:
    logger = logging.getLogger(__name__)

    @classmethod
    def setup_class(cls):
        """Initialize logger and set up WebDriver."""
        cls.logger = logging.getLogger(__name__)
        cls.driver = cls.get_driver()

    @classmethod
    def get_driver(cls):
        """Create and return a Selenium WebDriver instance."""
        try:
            chrome_options = cls.get_web_driver_options()
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.maximize_window()

            return driver

        except Exception as e:
            cls.logger.error(f"Failed to create WebDriver: {e}")
            raise

    @staticmethod
    def driver_dispose(driver):
        """Safely dispose of the WebDriver instance."""
        if driver:
            try:
                driver.quit()
            except Exception as e:
                TestSuitBase.logger.error(f"Error disposing driver: {e}")

    @classmethod
    def get_web_driver_options(cls):
        """Configure and return WebDriver options."""
        options = ChromeOptions()
        options.add_argument('--lang=en-GB')
        options.add_argument('--accept-language=en-US,en;q=0.9')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')

        return options
