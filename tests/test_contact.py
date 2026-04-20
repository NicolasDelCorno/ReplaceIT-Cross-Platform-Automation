import pytest
from pages.contact_page import ContactPage


@pytest.mark.ui
class TestContactPage:
    @pytest.fixture(autouse=True)
    def load_page(self, page, base_url):
        page.goto(f"{base_url}/contacto", wait_until="networkidle")
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

    def test_submit_empty_form_stays_on_page(self, page, base_url):
        self.contact.submit_form()
        assert page.url == f"{base_url}/contacto"
        # Strengthen: ensure native HTML validation marks required fields invalid
        assert self.contact.get_name_field().evaluate("el => el.matches(':invalid')") is True
        assert self.contact.get_email_field().evaluate("el => el.matches(':invalid')") is True
        assert self.contact.get_reason_field().evaluate("el => el.matches(':invalid')") is True

    def test_submit_with_invalid_email(self, page, base_url):
        self.contact.fill_form(name="Test User", email="not-an-email", reason="Testing")
        self.contact.submit_form()
        # Browser native validation should block submission
        assert page.url == f"{base_url}/contacto"
        assert self.contact.get_email_field().evaluate("el => el.matches(':invalid')") is True

    def test_submit_valid_form(self, page, base_url):
        self.contact.fill_form(
            name="Test User",
            email="test@example.com",
            reason="Automated test submission",
        )
        self.contact.submit_form()
        assert f"{base_url}/contacto" in page.url
        self.contact.wait_for_success_banner()
        assert self.contact.get_success_banner().is_visible()
