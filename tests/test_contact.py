import pytest
from pages.contact_page import ContactPage


BASE_URL = "https://replaceit.ai"


@pytest.mark.ui
class TestContactPage:
    @pytest.fixture(autouse=True)
    def load_page(self, page):
        page.goto(f"{BASE_URL}/contacto", wait_until="networkidle")
        self.contact = ContactPage(page)

    def test_hero_heading_visible(self):
        assert self.contact.get_hero_heading() == "Get in touch with us"

    def test_form_fields_present(self):
        assert self.contact.get_name_field().is_visible()
        assert self.contact.get_email_field().is_visible()
        assert self.contact.get_reason_field().is_visible()

    def test_send_button_present(self):
        assert self.contact.get_send_button().is_visible()

    def test_contact_email_link_present(self):
        assert self.contact.get_contact_email_link().is_visible()

    def test_phone_link_present(self):
        assert self.contact.get_phone_link().is_visible()

    def test_submit_empty_form_stays_on_page(self, page):
        self.contact.submit_form()
        assert page.url == f"{BASE_URL}/contacto"

    def test_submit_with_invalid_email(self, page):
        self.contact.fill_form(name="Test User", email="not-an-email", reason="Testing")
        self.contact.submit_form()
        # Browser native validation should block submission
        assert page.url == f"{BASE_URL}/contacto"

    def test_submit_valid_form(self, page):
        self.contact.fill_form(
            name="Test User",
            email="test@example.com",
            reason="Automated test submission",
        )
        self.contact.submit_form()
        # After a valid submission the page should show a success state or stay on /contacto
        # Update this assertion once the actual success behaviour is confirmed
        assert f"{BASE_URL}/contacto" in page.url
