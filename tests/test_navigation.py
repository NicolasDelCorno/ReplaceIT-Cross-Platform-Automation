import pytest
from pages.base_page import BasePage


@pytest.mark.ui
class TestNavigation:
    def test_nav_home_link(self, page, base_url):
        base = BasePage(page)
        page.goto(f"{base_url}/servicios", wait_until="networkidle")
        base.click_nav_home()
        page.wait_for_url(f"{base_url}/")
        assert page.url == f"{base_url}/"

    def test_nav_services_link(self, page, base_url):
        base = BasePage(page)
        page.goto(base_url, wait_until="networkidle")
        base.click_nav_services()
        page.wait_for_url(f"{base_url}/servicios")
        assert page.url == f"{base_url}/servicios"

    def test_nav_about_link(self, page, base_url):
        base = BasePage(page)
        page.goto(base_url, wait_until="networkidle")
        base.click_nav_about()
        page.wait_for_url(f"{base_url}/quienes-somos")
        assert page.url == f"{base_url}/quienes-somos"

    def test_nav_contact_link(self, page, base_url):
        base = BasePage(page)
        page.goto(base_url, wait_until="networkidle")
        base.click_nav_contact()
        page.wait_for_url(f"{base_url}/contacto")
        assert page.url == f"{base_url}/contacto"

    def test_logo_navigates_home(self, page, base_url):
        base = BasePage(page)
        page.goto(f"{base_url}/quienes-somos", wait_until="networkidle")
        base.click_logo()
        page.wait_for_url(f"{base_url}/")
        assert page.url == f"{base_url}/"

    @pytest.mark.parametrize("path", [
        "/",
        "/servicios",
        "/quienes-somos",
        "/contacto",
    ])
    def test_all_pages_load(self, page, base_url, path):
        expected_url = f"{base_url}{path}" if path != "/" else f"{base_url}/"
        page.goto(f"{base_url}{path}", wait_until="networkidle")
        assert page.url == expected_url
        assert page.locator("h1").first.is_visible()
