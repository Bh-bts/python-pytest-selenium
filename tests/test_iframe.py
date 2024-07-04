import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def setup(request):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://practice.expandtesting.com/")
    request.cls.driver = driver
    yield driver


class TestIFrame:
    def test_iframe(self, setup):
        driver = setup
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 10)

        iframe_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[href="/iframe"]')))
        driver.execute_script("arguments[0].click()", iframe_link)
        driver.switch_to.frame(driver.find_element(By.ID, "mce_0_ifr"))
        input_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body[id="tinymce"] > p')))
        driver.execute_script("arguments[0].scrollIntoView();", input_field)
        input_field.clear()
        input_field.send_keys("Test iFrame")
