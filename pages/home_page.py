from pages.base_page import BasePage


class HomePage(BasePage):
    def get_hero_heading(self):
        return self.page.locator("h1").first.inner_text().strip()

    def get_results_section(self):
        return self.page.locator("h2", has_text="Our Results")

    def get_engagement_section(self):
        return self.page.locator("h2", has_text="Engagement Models")

    def get_clients_section(self):
        return self.page.locator("h3", has_text="Clients")

    def click_view_services(self):
        self.page.locator("a[href='/servicios']", has_text="View services").click()
