from pages.base_page import BasePage


class AboutPage(BasePage):
    def get_hero_heading(self):
        return self.page.locator("h1").first.inner_text().strip()

    def get_gallery_section(self):
        return self.page.locator("h3", has_text="Gallery")
