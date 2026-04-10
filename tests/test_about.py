import pytest
from pages.about_page import AboutPage


BASE_URL = "https://replaceit.ai"


@pytest.mark.ui
class TestAboutPage:
    @pytest.fixture(autouse=True)
    def load_page(self, page):
        page.goto(f"{BASE_URL}/quienes-somos", wait_until="networkidle")
        self.about = AboutPage(page)

    def test_hero_heading_visible(self):
        assert self.about.get_hero_heading() == "About us"

    def test_gallery_section_visible(self):
        assert self.about.get_gallery_section().is_visible()
