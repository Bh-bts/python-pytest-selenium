import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.makemytrip.com/hotels/")
    request.cls.driver = driver
    yield driver


class TestMakeMyTrip:
    def test_make_my_trip(self, setup):
        driver = setup
        wait = WebDriverWait(driver, 10)

        price_per_night = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "label[for='appliedFilter']")))
        price_per_night.click()

        list_item = wait.until(EC.visibility_of_element_located((By.XPATH, "//li[text()='₹1500-₹2500']")))
        list_item.click()
        time.sleep(5)
