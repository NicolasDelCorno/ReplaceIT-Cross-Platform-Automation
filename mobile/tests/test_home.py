import pytest
from pages.home_page import HomePage


@pytest.mark.mobile
class TestHomePage:
    @pytest.fixture(autouse=True)
    def load_page(self, driver, base_url):
        driver.get(base_url)
        self.home = HomePage(driver)
        self.driver = driver

    def test_hero_heading_visible(self):
        assert self.home.get_hero_heading() == "Algorithms to impact your business"

    def test_clients_section_visible(self):
        assert self.home.get_clients_section().is_displayed()

    def test_results_section_visible(self):
        assert self.home.get_results_section().is_displayed()

    def test_engagement_section_visible(self):
        assert self.home.get_engagement_section().is_displayed()

    def test_view_services_cta_navigates(self, base_url):
        self.home.click_view_services()
        self.home.wait_for_url(f"{base_url}/servicios")
        assert self.driver.current_url == f"{base_url}/servicios"
