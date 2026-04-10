from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class HomePage(BasePage):
    def get_hero_heading(self):
        return self.get_h1()

    def get_clients_section(self):
        element = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(., 'Clients')]"))
        )
        self.scroll_to(element)
        self.wait.until(EC.visibility_of(element))
        return element

    def get_results_section(self):
        element = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(., 'Our Results')]"))
        )
        self.scroll_to(element)
        # Confirm is_displayed() will be True
        self.wait.until(EC.visibility_of(element))
        return element

    def get_engagement_section(self):
        element = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(., 'Engagement Models')]"))
        )
        self.scroll_to(element)
        self.wait.until(EC.visibility_of(element))
        return element

    def click_view_services(self):
        element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[@href='/servicios' and contains(., 'View services')]")
            )
        )
        self.scroll_to(element)
        self.js_click(element)
