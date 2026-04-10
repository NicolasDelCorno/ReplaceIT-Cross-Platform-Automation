from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AboutPage(BasePage):
    def get_hero_heading(self):
        return self.get_h1()

    def get_gallery_section(self):
        element = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(., 'Gallery')]"))
        )
        self.scroll_to(element)
        self.wait.until(EC.visibility_of(element))
        return element
