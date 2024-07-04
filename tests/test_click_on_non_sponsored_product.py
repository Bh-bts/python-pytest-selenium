import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope='class')
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://amazon.in")
    request.cls.driver = driver
    yield driver


class Test_Click_on_non_sponsored_product:

    @pytest.mark.usefixtures('setup')
    def test_click_on_non_sponsored_product(self, setup):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        search_input = wait.until(EC.visibility_of_element_located((By.ID, "twotabsearchtextbox")))
        search_input.send_keys('iPhone 15')
        search_input.submit()

        product_titles = driver.find_elements(By.XPATH, "//div[@data-cy='title-recipe']")

        for product_title in product_titles:
            if product_title.find_elements(By.XPATH, './div'):
                continue

            else:
                product_title_link = product_title.find_element(By.XPATH, './/h2//a[contains(@class, "a-link-normal")]')
                product_title_link.click()
                break

        assert "ref=sr_1_sspa" not in driver.current_url
