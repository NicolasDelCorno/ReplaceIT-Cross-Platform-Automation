import pytest
from pages.services_page import ServicesPage, EXPECTED_SERVICES_IOS, EXPECTED_SERVICES_ANDROID


def _expected(request):
    platform = request.config.getoption("--platform", default="ios")
    return EXPECTED_SERVICES_ANDROID if platform == "android" else EXPECTED_SERVICES_IOS


@pytest.mark.mobile
class TestServicesPage:
    @pytest.fixture(autouse=True)
    def load_page(self, driver, request, base_url):
        driver.get(f"{base_url}/servicios")
        self.services = ServicesPage(driver)
        self.expected = _expected(request)

    def test_hero_heading_visible(self):
        assert self.services.get_hero_heading() == "We create digital products"

    def test_all_service_cards_present(self):
        headings = self.services.get_service_headings()
        for service in self.expected:
            assert service in headings, f"Service card '{service}' not found"

    def test_service_card_count(self):
        apply_links = self.services.get_apply_now_links()
        assert len(apply_links) == len(self.expected)

    @pytest.mark.parametrize("index", range(len(EXPECTED_SERVICES_ANDROID)))
    def test_apply_now_navigates_to_contact(self, driver, request, base_url, index):
        expected = _expected(request)
        if index >= len(expected):
            pytest.skip("index out of range for this platform")
        driver.get(f"{base_url}/servicios")
        services = ServicesPage(driver)
        services.click_apply_now(index)
        services.wait_for_url(f"{base_url}/contacto")
        assert driver.current_url == f"{base_url}/contacto"
