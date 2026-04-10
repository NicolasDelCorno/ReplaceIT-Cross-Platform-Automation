import pytest
from pages.about_page import AboutPage


BASE_URL = "https://replaceit.ai"


@pytest.mark.mobile
class TestAboutPage:
    @pytest.fixture(autouse=True)
    def load_page(self, driver):
        driver.get(f"{BASE_URL}/quienes-somos")
        self.about = AboutPage(driver)

    def test_hero_heading_visible(self):
        assert self.about.get_hero_heading() == "About us"

    def test_gallery_section_visible(self):
        assert self.about.get_gallery_section().is_displayed()
