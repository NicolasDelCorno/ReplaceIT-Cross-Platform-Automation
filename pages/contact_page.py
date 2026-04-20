from pages.base_page import BasePage


class ContactPage(BasePage):
    SUCCESS_BANNER_TEXT = "Thank you! Your details have been sent successfully"

    def get_hero_heading(self):
        return self.page.locator("h1").first.inner_text().strip()

    def get_name_field(self):
        return self.page.locator("input[name='nombreyapellido']")

    def get_email_field(self):
        return self.page.locator("input[name='email']")

    def get_reason_field(self):
        return self.page.locator("input[name='motivo']")

    def get_send_button(self):
        return self.page.locator("button", has_text="Send")

    def fill_form(self, name="", email="", reason=""):
        if name:
            self.get_name_field().fill(name)
        if email:
            self.get_email_field().fill(email)
        if reason:
            self.get_reason_field().fill(reason)

    def submit_form(self):
        self.get_send_button().click()

    def get_success_banner(self):
        # Keep selector flexible: assert on the user-visible text
        return self.page.get_by_text(self.SUCCESS_BANNER_TEXT, exact=False).first

    def wait_for_success_banner(self, timeout_ms: int = 15000):
        self.get_success_banner().wait_for(state="visible", timeout=timeout_ms)

    def get_contact_email_link(self):
        return self.page.locator("a[href='mailto:hello@replace.com.ar']")

    def get_phone_link(self):
        return self.page.locator("a[href='tel:+542235064735']")
