import pytest
from pages.services_page import ServicesPage, EXPECTED_SERVICES


@pytest.mark.ui
class TestServicesPage:
    @pytest.fixture(autouse=True)
    def load_page(self, page, base_url):
        page.goto(f"{base_url}/servicios", wait_until="networkidle")
        self.services = ServicesPage(page)

    def test_hero_heading_visible(self):
        assert self.services.get_hero_heading() == "We create digital products"

    def test_all_service_cards_present(self):
        headings = self.services.get_service_headings()
        for service in EXPECTED_SERVICES:
            assert service in headings, f"Service card '{service}' not found"

    def test_service_card_count(self):
        apply_links = self.services.get_apply_now_links()
        assert len(apply_links) == len(EXPECTED_SERVICES)

    @pytest.mark.parametrize("index", range(len(EXPECTED_SERVICES)))
    def test_apply_now_navigates_to_contact(self, page, base_url, index):
        # Re-load page for each parametrized run since navigation changes the URL
        page.goto(f"{base_url}/servicios", wait_until="networkidle")
        services = ServicesPage(page)
        services.click_apply_now(index)
        page.wait_for_url(f"{base_url}/contacto")
        assert page.url == f"{base_url}/contacto"
