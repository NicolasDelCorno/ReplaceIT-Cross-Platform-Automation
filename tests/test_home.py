import pytest
from pages.home_page import HomePage


@pytest.mark.ui
class TestHomePage:
    @pytest.fixture(autouse=True)
    def load_page(self, page, base_url):
        page.goto(base_url, wait_until="networkidle")
        self.home = HomePage(page)

    def test_hero_heading_visible(self):
        assert self.home.get_hero_heading() == "Algorithms to impact your business"

    def test_clients_section_visible(self):
        assert self.home.get_clients_section().is_visible()

    def test_results_section_visible(self):
        assert self.home.get_results_section().is_visible()

    def test_engagement_section_visible(self):
        assert self.home.get_engagement_section().is_visible()

    def test_view_services_cta_navigates(self, page, base_url):
        self.home.click_view_services()
        page.wait_for_url(f"{base_url}/servicios")
        assert page.url == f"{base_url}/servicios"
