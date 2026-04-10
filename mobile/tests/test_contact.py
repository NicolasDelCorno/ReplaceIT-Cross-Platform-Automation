import pytest
from pages.contact_page import ContactPage


BASE_URL = "https://replaceit.ai"


@pytest.mark.mobile
class TestContactPage:
    @pytest.fixture(autouse=True)
    def load_page(self, driver):
        driver.get(f"{BASE_URL}/contacto")
        self.contact = ContactPage(driver)

    def test_hero_heading_visible(self):
        assert self.contact.get_hero_heading() == "Get in touch with us"

    def test_form_fields_present(self):
        assert self.contact.get_name_field().is_displayed()
        assert self.contact.get_email_field().is_displayed()
        assert self.contact.get_reason_field().is_displayed()

    def test_send_button_present(self):
        assert self.contact.get_send_button().is_displayed()

    def test_contact_email_link_present(self):
        assert self.contact.get_contact_email_link().is_displayed()

    def test_phone_link_present(self):
        assert self.contact.get_phone_link().is_displayed()

    def test_submit_empty_form_stays_on_page(self):
        self.contact.submit_form()
        assert self.contact.current_url() == f"{BASE_URL}/contacto"

    def test_submit_with_invalid_email(self):
        self.contact.fill_form(name="Test User", email="not-an-email", reason="Testing")
        self.contact.submit_form()
        assert self.contact.current_url() == f"{BASE_URL}/contacto"

    def test_submit_valid_form(self):
        self.contact.fill_form(
            name="Test User",
            email="test@example.com",
            reason="Automated test submission",
        )
        self.contact.submit_form()
        assert f"{BASE_URL}/contacto" in self.contact.current_url()
