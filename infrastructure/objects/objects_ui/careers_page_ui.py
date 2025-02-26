from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By

from infrastructure.Infra.dal.web_driver_extension.web_driver_extension import DriverEX
from infrastructure.objects.objects_ui.career_page_ui import CareerPageUi


class CareersPageUi:
    def __init__(self, driver: webdriver, career_page: CareerPageUi = None) -> None:
        self.__driver = driver
        if career_page is None:
            self.__career_page = CareerPageUi(driver)
        else:
            self.__career_page = career_page

        # locators
        self.__apply_now_link_ext = (By.XPATH,
                                     "//tr[not(@class='hidden-department')]//a[.='Apply now']")

    def apply_to_all_jobs_same_tab(self, form_fields: dict[str, str]) -> None:
        try:
            apply_now_buttons = DriverEX.search_elements(
                driver=self.__driver,
                by=self.__apply_now_link_ext)

            total_buttons = len(apply_now_buttons)
            print(f"Found {total_buttons} 'Apply now' buttons")

            for index in range(total_buttons):
                try:
                    print(f"Applying for job {index + 1} of {total_buttons}")

                    DriverEX.force_click(
                        driver=self.__driver,
                        by=self.__apply_now_link_ext,
                        element=apply_now_buttons[index])

                    self.__career_page = CareerPageUi(self.__driver)

                    self.__career_page.fill_application_form(form_fields) \
                        .upload_resume()

                    self.__driver.back()

                except Exception as e:
                    print(f"Error in apply_to_all_jobs: {str(e)}")
                    raise

        except Exception as e:
            print(f"Error in apply_to_all_jobs: {str(e)}")
            raise

    def apply_to_all_jobs_new_tab(self, form_fields: dict[str, str]) -> None:
        try:
            apply_now_buttons = DriverEX.search_elements(
                driver=self.__driver,
                by=self.__apply_now_link_ext)

            total_buttons = len(apply_now_buttons)
            print(f"Found {total_buttons} 'Apply now' buttons")

            for index in range(total_buttons):
                try:
                    print(f"Applying for job {index + 1} of {total_buttons}")

                    element_link =DriverEX.search_element(\
                        driver=self.__driver,\
                        by=self.__apply_now_link_ext)\
                        .get_attribute("href")

                    self.__career_page = CareerPageUi(self.__driver)

                    self.__driver.execute_script(f"window.open('{element_link}', '_blank');")
                    self.__driver.switch_to.window(self.__driver.window_handles[1])

                    self.__career_page.fill_application_form(form_fields) \
                        .upload_resume()

                    self.__driver.close()
                    self.__driver.switch_to.window(self.__driver.window_handles[0])

                except Exception as e:
                    print(f"Error in apply_to_all_jobs: {str(e)}")
                    raise

        except Exception as e:
            print(f"Error in apply_to_all_jobs: {str(e)}")
            raise
