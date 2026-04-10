import pytest
from pages.base_page import BasePage


BASE_URL = "https://replaceit.ai"


@pytest.mark.ui
class TestNavigation:
    def test_nav_home_link(self, page):
        base = BasePage(page)
        page.goto(f"{BASE_URL}/servicios", wait_until="networkidle")
        base.click_nav_home()
        page.wait_for_url(f"{BASE_URL}/")
        assert page.url == f"{BASE_URL}/"

    def test_nav_services_link(self, page):
        base = BasePage(page)
        page.goto(BASE_URL, wait_until="networkidle")
        base.click_nav_services()
        page.wait_for_url(f"{BASE_URL}/servicios")
        assert page.url == f"{BASE_URL}/servicios"

    def test_nav_about_link(self, page):
        base = BasePage(page)
        page.goto(BASE_URL, wait_until="networkidle")
        base.click_nav_about()
        page.wait_for_url(f"{BASE_URL}/quienes-somos")
        assert page.url == f"{BASE_URL}/quienes-somos"

    def test_nav_contact_link(self, page):
        base = BasePage(page)
        page.goto(BASE_URL, wait_until="networkidle")
        base.click_nav_contact()
        page.wait_for_url(f"{BASE_URL}/contacto")
        assert page.url == f"{BASE_URL}/contacto"

    def test_logo_navigates_home(self, page):
        base = BasePage(page)
        page.goto(f"{BASE_URL}/quienes-somos", wait_until="networkidle")
        base.click_logo()
        page.wait_for_url(f"{BASE_URL}/")
        assert page.url == f"{BASE_URL}/"

    @pytest.mark.parametrize("path,expected_url", [
        ("/", f"{BASE_URL}/"),
        ("/servicios", f"{BASE_URL}/servicios"),
        ("/quienes-somos", f"{BASE_URL}/quienes-somos"),
        ("/contacto", f"{BASE_URL}/contacto"),
    ])
    def test_all_pages_load(self, page, path, expected_url):
        page.goto(f"{BASE_URL}{path}", wait_until="networkidle")
        assert page.url == expected_url
        assert page.locator("h1").first.is_visible()
