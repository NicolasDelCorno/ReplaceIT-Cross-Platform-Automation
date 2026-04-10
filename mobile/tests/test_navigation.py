import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


BASE_URL = "https://replaceit.ai"


@pytest.mark.mobile
class TestNavigation:
    def test_nav_home_link(self, driver):
        base = BasePage(driver)
        driver.get(f"{BASE_URL}/servicios")
        base.click_nav_home()
        base.wait_for_url(f"{BASE_URL}/")
        assert driver.current_url == f"{BASE_URL}/"

    def test_nav_services_link(self, driver):
        base = BasePage(driver)
        driver.get(BASE_URL)
        base.click_nav_services()
        base.wait_for_url(f"{BASE_URL}/servicios")
        assert driver.current_url == f"{BASE_URL}/servicios"

    def test_nav_about_link(self, driver):
        base = BasePage(driver)
        driver.get(BASE_URL)
        base.click_nav_about()
        base.wait_for_url(f"{BASE_URL}/quienes-somos")
        assert driver.current_url == f"{BASE_URL}/quienes-somos"

    def test_nav_contact_link(self, driver):
        base = BasePage(driver)
        driver.get(BASE_URL)
        base.click_nav_contact()
        base.wait_for_url(f"{BASE_URL}/contacto")
        assert driver.current_url == f"{BASE_URL}/contacto"

    def test_logo_navigates_home(self, driver):
        base = BasePage(driver)
        driver.get(f"{BASE_URL}/quienes-somos")
        base.click_logo()
        base.wait_for_url(f"{BASE_URL}/")
        assert driver.current_url == f"{BASE_URL}/"

    @pytest.mark.parametrize("path,expected_url", [
        ("/", f"{BASE_URL}/"),
        ("/servicios", f"{BASE_URL}/servicios"),
        ("/quienes-somos", f"{BASE_URL}/quienes-somos"),
        ("/contacto", f"{BASE_URL}/contacto"),
    ])
    def test_all_pages_load(self, driver, path, expected_url):
        driver.get(f"{BASE_URL}{path}")
        assert driver.current_url == expected_url
        h1 = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        assert h1.is_displayed()
