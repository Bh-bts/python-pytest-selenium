import pytest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope='class')
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://google.com")
    request.cls.driver = driver
    yield driver


@pytest.mark.usefixtures('setup')
class TestNonSponsoredAmazonLink:

    def test_verify_user_click_on_non_sponsored_amazon_link(self):
        driver = self.driver
        wait = WebDriverWait(driver, 30)

        search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea[name='q']")))
        search_input.send_keys('Amazon')
        search_input.send_keys(Keys.ENTER)

        wait.until(EC.visibility_of_element_located((By.XPATH, "//a")))
        all_links = driver.find_elements(By.XPATH, "//a")

        for link in all_links:
            link_text = link.text
            link_attribute = link.get_attribute("data-rw")
            if 'Amazon.in' in link_text and not link_attribute:
                link.click()
                break

        assert driver.current_url == 'https://www.amazon.in/'
