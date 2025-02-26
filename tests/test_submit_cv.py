import pytest
from selenium import webdriver

from infrastructure.Infra.dal.data_reposetory.data_rep import DataRep
from infrastructure.objects.objects_ui.filters_ui import FiltersUi
from infrastructure.objects.objects_ui.home_page_ui import HomePageUi


@pytest.mark.usefixtures("chrome_web_driver_base")
class TestSubmitCv:
    def test_submit_cv(self, chrome_web_driver_base: webdriver.Chrome):
        chrome_web_driver_base.get(DataRep.connecteam_url)

        apply_form_parameters: dict[str, str] = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890"
        }

        home_page_ui = HomePageUi(chrome_web_driver_base)
        filters = FiltersUi(chrome_web_driver_base)

        # NOT RECOMMENDED: OPEN FORM IN THE SAME TAB
        # 1. Relay on index - possible out of range -
        # need to assume the total number does not change on "Back"
        # 2. Performs search for the same elements for every iteration (to avoid StaleElement)
        # 3. When click 'Back' it is possible to lose the original state of the page
        careers_page = home_page_ui \
            .click_on_careers_link()

        filters.select_department_filter(filter_value="R&D")

        careers_page\
         .apply_to_all_jobs_same_tab(form_fields=apply_form_parameters)

        # RECOMMENDED: OPEN FORM IN A NEW TAB
        # 1. Does not use index - uses cached elements
        # 2. Open link in new tab and switch context
        # - this avoid StaleElement and keep the original state of the page
        careers_page = home_page_ui \
            .click_on_careers_link()

        filters.select_department_filter(filter_value="R&D")

        careers_page \
            .apply_to_all_jobs_new_tab(form_fields=apply_form_parameters)



