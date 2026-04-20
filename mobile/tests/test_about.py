import pytest
from pages.about_page import AboutPage


@pytest.mark.mobile
class TestAboutPage:
    @pytest.fixture(autouse=True)
    def load_page(self, driver, base_url):
        driver.get(f"{base_url}/quienes-somos")
        self.about = AboutPage(driver)

    def test_hero_heading_visible(self):
        assert self.about.get_hero_heading() == "About us"

    def test_gallery_section_visible(self):
        assert self.about.get_gallery_section().is_displayed()
