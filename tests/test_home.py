import pytest
from pages.home_page import HomePage


BASE_URL = "https://replaceit.ai"


@pytest.mark.ui
class TestHomePage:
    @pytest.fixture(autouse=True)
    def load_page(self, page):
        page.goto(BASE_URL, wait_until="networkidle")
        self.home = HomePage(page)

    def test_hero_heading_visible(self):
        assert self.home.get_hero_heading() == "Algorithms to impact your business"

    def test_clients_section_visible(self):
        assert self.home.get_clients_section().is_visible()

    def test_results_section_visible(self):
        assert self.home.get_results_section().is_visible()

    def test_engagement_section_visible(self):
        assert self.home.get_engagement_section().is_visible()

    def test_view_services_cta_navigates(self, page):
        self.home.click_view_services()
        page.wait_for_url(f"{BASE_URL}/servicios")
        assert page.url == f"{BASE_URL}/servicios"
