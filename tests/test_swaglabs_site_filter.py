import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope='class')
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")
    request.cls.driver = driver
    yield driver


@pytest.mark.usefixtures('setup')
class Test_login_with_valid_user:

    @pytest.fixture(scope='function', autouse=True)
    def test_login_with_valid_user(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        username_input = wait.until(EC.visibility_of_element_located((By.ID, 'user-name')))
        username_input.send_keys('standard_user')

        password_input = wait.until(EC.visibility_of_element_located((By.ID, 'password')))
        password_input.send_keys('secret_sauce')

        login_button = wait.until(EC.visibility_of_element_located((By.ID, "login-button")))
        login_button.click()

        assert driver.current_url == 'https://www.saucedemo.com/inventory.html'

    def test_verify_product_price_sorting_from_low_to_high(self):
        apply_filter = 'Price (low to high)'

        select = Select(self.driver.find_element(By.CSS_SELECTOR, "select[class='product_sort_container']"))
        select.select_by_visible_text(apply_filter)

        products_price = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="inventory_item_price"]')

        is_sorted = True
        for i in range(len(products_price) - 1):
            price1 = float(products_price[i].text.replace('$', ''))
            price2 = float(products_price[i + 1].text.replace('$', ''))
            if price1 > price2:
                is_sorted = False
                break

        assert is_sorted, "Product prices are not sorted from low to high"

    def test_verify_product_price_sorting_from_high_to_low(self):
        apply_filter = 'Price (high to low)'

        select = Select(self.driver.find_element(By.CSS_SELECTOR, "select[class='product_sort_container']"))
        select.select_by_visible_text(apply_filter)

        products_price = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="inventory_item_price"]')

        is_sorted = True
        for i in range(len(products_price) - 1):
            price1 = float(products_price[i].text.replace('$', ''))
            price2 = float(products_price[i].text.replace('$', ''))

            if price1 < price2:
                is_sorted = False
                break

        assert is_sorted, 'Product prices are not sorted from high to low'

    def test_verify_product_name_sorting_from_a_to_z(self):
        apply_filter = 'Name (A to Z)'

        select = Select(self.driver.find_element(By.CSS_SELECTOR, "select[class='product_sort_container']"))
        select.select_by_visible_text(apply_filter)

        products_name = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="inventory_item_name "]')

        is_sorted = True

        for i in range(len(products_name) - 1):
            name1 = products_name[i].text
            name2 = products_name[i + 1].text
            if name1 > name2:
                is_sorted = False
                break

        assert is_sorted, 'Product names are not sorted from A to Z'

    def test_verify_product_name_sorting_from_z_to_a(self):
        apply_filter = 'Name (Z to A)'

        select = Select(self.driver.find_element(By.CSS_SELECTOR, "select[class='product_sort_container']"))
        select.select_by_visible_text(apply_filter)

        products_name = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="inventory_item_name "]')

        is_sorted = True

        for i in range(len(products_name) - 1):
            name1 = products_name[i].text
            name2 = products_name[i + 1].text

            if name1 < name2:
                is_sorted = False
                break

        assert is_sorted, 'Product prices are not sorted from Z to Z'

    def test_verify_adding_product_to_cart(self):
        product_name = 'Test.allTheThings() T-Shirt (Red)'

        add_to_cart_button_from_product_name_text = self.driver.find_element(By.XPATH,
                                                                             "//div[text()='" + product_name + "']//ancestor::div[@class='inventory_item']//button")
        add_to_cart_button_from_product_name_text.click()

        cart_link = self.driver.find_element(By.CSS_SELECTOR, "a[class='shopping_cart_link']")
        cart_link.click()

        product_name_in_cart = self.driver.find_element(By.XPATH, "//a/div[text()='" + product_name + "']")
        assert product_name_in_cart.text == product_name

        checkout_button = self.driver.find_element(By.ID, 'checkout')
        checkout_button.click()

        first_name_input = self.driver.find_element(By.ID, 'first-name')
        first_name_input.send_keys('Test')

        last_name_input = self.driver.find_element(By.ID, 'last-name')
        last_name_input.send_keys('QA')

        postal_code = self.driver.find_element(By.ID, 'postal-code')
        postal_code.send_keys('269874')

        continue_button = self.driver.find_element(By.ID, 'continue')
        continue_button.click()

        finish_button = self.driver.find_element(By.ID, 'finish')
        finish_button.click()

        order_confirmation_text = self.driver.find_element(By.CSS_SELECTOR, 'h2[class="complete-header"]')
        assert order_confirmation_text.text == 'Thank you for your order!'
