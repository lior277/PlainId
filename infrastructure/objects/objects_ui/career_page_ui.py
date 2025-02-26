import os

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from infrastructure.Infra.dal.web_driver_extension.web_driver_extension import DriverEX


class CareerPageUi:
    def __init__(self, driver: webdriver) -> None:
        self.__driver = driver
        self.__field_name = "input[id='{field_name}']"
        self.__project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self.__resume_path = os.path.join(self.__project_root, 'example_cv.pdf')
        self.__in_iframe = False

        # locators
        self.__upload_resume_ext = (By.CSS_SELECTOR, "input[type='file']")
        self.__iframe_ext = (By.CSS_SELECTOR, "iframe[id='grnhse_iframe']")


    def fill_application_form(self, form_fields: dict[str, str]):
        try:
            DriverEX.switch_to_iframe(driver=self.__driver, by=self.__iframe_ext)

            for field_name, field_value in form_fields.items():
                field_name_ext = (By.CSS_SELECTOR, self.__field_name.format(field_name=field_name))

                DriverEX.send_keys_auto(
                    driver=self.__driver,
                    by=field_name_ext,
                    input_text=field_value)

            DriverEX.switch_to_default_content(driver=self.__driver)
            return self

        except Exception as e:
            DriverEX.switch_to_default_content(driver=self.__driver)
            raise e

    def upload_resume(self):
        DriverEX.switch_to_iframe(driver=self.__driver, by=self.__iframe_ext)
        try:

            if not os.path.exists(self.__resume_path):
                raise FileNotFoundError(f"Resume file not found at: {self.__resume_path}")

            DriverEX.upload_file(driver=self.__driver, by=self.__upload_resume_ext, input_text=self.__resume_path)
            DriverEX.switch_to_default_content(driver=self.__driver)
            return self

        except Exception as e:
            print(f"Error uploading resume: {str(e)}")
            DriverEX.switch_to_default_content(driver=self.__driver)
            raise e