from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class ContactPage(BasePage):
    SUCCESS_BANNER_TEXT = "Thank you! Your details have been sent successfully"
    SUCCESS_BANNER_KEYWORD = "Thank you"

    def get_hero_heading(self):
        return self.get_h1()

    def _scroll_and_confirm(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.scroll_to(element)
        self.wait.until(EC.visibility_of(element))
        return element

    def get_name_field(self):
        return self._scroll_and_confirm((By.CSS_SELECTOR, "input[name='nombreyapellido']"))

    def get_email_field(self):
        return self._scroll_and_confirm((By.CSS_SELECTOR, "input[name='email']"))

    def get_reason_field(self):
        return self._scroll_and_confirm((By.CSS_SELECTOR, "input[name='motivo']"))

    def get_send_button(self):
        return self._scroll_and_confirm((By.XPATH, "//button[contains(., 'Send')]"))

    def get_contact_email_link(self):
        return self._scroll_and_confirm((By.CSS_SELECTOR, "a[href='mailto:hello@replace.com.ar']"))

    def get_phone_link(self):
        return self._scroll_and_confirm((By.CSS_SELECTOR, "a[href='tel:+542235064735']"))

    def fill_form(self, name="", email="", reason=""):
        if name:
            field = self.get_name_field()
            field.clear()
            field.send_keys(name)
        if email:
            field = self.get_email_field()
            field.clear()
            field.send_keys(email)
        if reason:
            field = self.get_reason_field()
            field.clear()
            field.send_keys(reason)

    def submit_form(self):
        self.js_click(self.get_send_button())

    def get_success_banner(self):
        locator = (By.XPATH, f"//*[contains(normalize-space(), '{self.SUCCESS_BANNER_KEYWORD}')]")
        long_wait = WebDriverWait(self.driver, 20)
        element = long_wait.until(EC.presence_of_element_located(locator))
        self.scroll_to(element)
        long_wait.until(EC.visibility_of(element))
        return element

    def element_check_validity(self, element):
        # HTML5 validity; returns True/False (works for mobile browsers too)
        return self.driver.execute_script("return arguments[0].checkValidity();", element)
