import pytest

from pages.base_page import BasePage


@pytest.mark.ui
class TestFooter:
    @pytest.fixture(autouse=True)
    def load_page(self, page, base_url):
        page.goto(base_url, wait_until="networkidle")
        self.base = BasePage(page)

    def test_privacy_policy_link_works(self, page):
        link = page.locator("footer a[href='#priv']").first
        assert link.is_visible()
        assert link.get_attribute("href") == "#priv"
        self.base.click_privacy_policy()
        assert page.url.endswith("/")

    def test_cookie_policy_link_works(self, page):
        link = page.locator("footer a[href='#cookies']").first
        assert link.is_visible()
        assert link.get_attribute("href") == "#cookies"
        self.base.click_cookie_policy()
        assert page.url.endswith("/")

    def test_terms_and_conditions_link_works(self, page):
        link = page.locator("footer a[href='#term']").first
        assert link.is_visible()
        assert link.get_attribute("href") == "#term"
        self.base.click_terms_and_conditions()
        assert page.url.endswith("/")

    @pytest.mark.parametrize("key", ["instagram", "facebook", "linkedin"])
    def test_social_links_present_in_footer(self, page, key):
        href = BasePage.SOCIAL_LINKS[key]
        link = self.base.get_footer_link(href).first
        assert link.is_visible()
        # If the link opens a new tab, ensure target is set correctly.
        target = link.get_attribute("target")
        if target is not None:
            assert target == "_blank"
