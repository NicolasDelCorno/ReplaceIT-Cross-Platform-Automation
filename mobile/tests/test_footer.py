import pytest

from pages.base_page import BasePage


@pytest.mark.mobile
class TestFooter:
    @pytest.fixture(autouse=True)
    def load_page(self, driver, base_url):
        driver.get(base_url)
        self.base = BasePage(driver)

    def test_privacy_policy_link_works(self, driver):
        link = self.base.get_footer_link("#priv")
        assert link.is_displayed()
        assert link.get_attribute("href").endswith("#priv")
        self.base.click_privacy_policy()

    def test_cookie_policy_link_works(self, driver):
        link = self.base.get_footer_link("#cookies")
        assert link.is_displayed()
        assert link.get_attribute("href").endswith("#cookies")
        self.base.click_cookie_policy()

    def test_terms_and_conditions_link_works(self, driver):
        link = self.base.get_footer_link("#term")
        assert link.is_displayed()
        assert link.get_attribute("href").endswith("#term")
        self.base.click_terms_and_conditions()

    @pytest.mark.parametrize("key", ["instagram", "facebook", "linkedin"])
    def test_social_links_present_in_footer(self, key):
        href = BasePage.SOCIAL_LINKS[key]
        link = self.base.get_footer_link(href)
        assert link.is_displayed()
        assert link.get_attribute("href") == href
