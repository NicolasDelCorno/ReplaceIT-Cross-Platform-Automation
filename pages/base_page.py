class BasePage:
    NAV_LINKS = {
        "home": "/",
        "services": "/servicios",
        "about": "/quienes-somos",
        "contact": "/contacto",
    }

    SOCIAL_LINKS = {
        "instagram": "https://www.instagram.com/",
        "facebook": "https://www.facebook.com/",
        "linkedin": "https://www.linkedin.com/company/replaceit/",
    }

    def __init__(self, page):
        self.page = page

    # ── Navigation ─────────────────────────────────────────────────────────────

    def click_nav_home(self):
        self.page.locator("nav a[href='/']").first.click()

    def click_nav_services(self):
        self.page.get_by_role("banner").get_by_role("link", name="Services").click()

    def click_nav_about(self):
        self.page.get_by_role("banner").get_by_role("link", name="About Us").click()

    def click_nav_contact(self):
        self.page.get_by_role("banner").get_by_role("link", name="Contact", exact=True).click()

    def click_logo(self):
        self.page.locator("header a[href='/']").first.click()

    # ── Footer ─────────────────────────────────────────────────────────────────

    def get_footer_link(self, href):
        return self.page.locator(f"footer a[href='{href}']")

    def click_privacy_policy(self):
        link = self.page.locator("footer a[href='#priv']").first
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        link.scroll_into_view_if_needed()
        link.click(force=True)

    def click_cookie_policy(self):
        link = self.page.locator("footer a[href='#cookies']").first
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        link.scroll_into_view_if_needed()
        link.click(force=True)

    def click_terms_and_conditions(self):
        link = self.page.locator("footer a[href='#term']").first
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        link.scroll_into_view_if_needed()
        link.click(force=True)

    # ── Helpers ────────────────────────────────────────────────────────────────

    def current_url(self):
        return self.page.url

    def get_h1(self):
        return self.page.locator("h1").first.inner_text().strip()
