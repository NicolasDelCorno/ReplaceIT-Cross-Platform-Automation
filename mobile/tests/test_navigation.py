import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


@pytest.mark.mobile
class TestNavigation:
    def test_nav_home_link(self, driver, base_url):
        base = BasePage(driver)
        driver.get(f"{base_url}/servicios")
        base.click_nav_home()
        base.wait_for_url(f"{base_url}/")
        assert driver.current_url == f"{base_url}/"

    def test_nav_services_link(self, driver, base_url):
        base = BasePage(driver)
        driver.get(base_url)
        base.click_nav_services()
        base.wait_for_url(f"{base_url}/servicios")
        assert driver.current_url == f"{base_url}/servicios"

    def test_nav_about_link(self, driver, base_url):
        base = BasePage(driver)
        driver.get(base_url)
        base.click_nav_about()
        base.wait_for_url(f"{base_url}/quienes-somos")
        assert driver.current_url == f"{base_url}/quienes-somos"

    def test_nav_contact_link(self, driver, base_url):
        base = BasePage(driver)
        driver.get(base_url)
        base.click_nav_contact()
        base.wait_for_url(f"{base_url}/contacto")
        assert driver.current_url == f"{base_url}/contacto"

    def test_logo_navigates_home(self, driver, base_url):
        base = BasePage(driver)
        driver.get(f"{base_url}/quienes-somos")
        base.click_logo()
        base.wait_for_url(f"{base_url}/")
        assert driver.current_url == f"{base_url}/"

    @pytest.mark.parametrize("path", [
        "/",
        "/servicios",
        "/quienes-somos",
        "/contacto",
    ])
    def test_all_pages_load(self, driver, base_url, path):
        expected_url = f"{base_url}{path}" if path != "/" else f"{base_url}/"
        driver.get(f"{base_url}{path}")
        assert driver.current_url == expected_url
        h1 = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        assert h1.is_displayed()
