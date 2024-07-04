import pytest

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://practice.expandtesting.com/')
    request.cls.driver = driver
    yield driver


@pytest.mark.usefixtures('setup')
class TestDragAndDrop:
    def test_drag_and_drop(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        drag_and_drop = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="/drag-and-drop"]')))
        driver.execute_script("arguments[0].click()", drag_and_drop)

        column_a = wait.until(EC.visibility_of_element_located((By.ID, 'column-a')))
        column_b = wait.until(EC.visibility_of_element_located((By.ID, 'column-b')))

        ActionChains(driver).drag_and_drop(column_a, column_b).perform()
        assert column_a.text == 'B'
