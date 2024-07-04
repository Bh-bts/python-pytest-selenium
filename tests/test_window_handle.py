import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://practice.expandtesting.com/")
    request.cls.driver = driver
    yield driver


class TestApp:
    def test_window_handle(self, setup):
        driver = setup
        driver.implicitly_wait(10)

        wait = WebDriverWait(driver, 10)

        multiple_window_link = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Multiple Windows']")))

        driver.execute_script("arguments[0].click()", multiple_window_link)
        click_here_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="/windows/new"]')))
        click_here_link.click()

        driver.switch_to.window(driver.window_handles[1])
        header_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1")))
        assert header_text.text == 'Example of a new window page for Automation Testing Practice'
