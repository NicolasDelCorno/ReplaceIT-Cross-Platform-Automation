from pages.base_page import BasePage


EXPECTED_SERVICES = [
    "Autonomous AI Agents",
    "Chatbots with RAG",
    "Computer Vision",
    "Process Automation",
    "Generative AI",
    "Recommendation Systems",
    "NLP & Sentiment Analysis",
]


class ServicesPage(BasePage):
    def get_hero_heading(self):
        return self.page.locator("h1").first.inner_text().strip()

    def get_service_cards(self):
        return self.page.locator("h3").all()

    def get_service_headings(self):
        return [h.inner_text().strip() for h in self.get_service_cards()]

    def get_apply_now_links(self):
        return self.page.locator("a[href='/contacto']").filter(has_text="Apply now").all()

    def click_apply_now(self, index=0):
        self.get_apply_now_links()[index].click()
