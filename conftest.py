import os
import pytest
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()


def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    reports_dir = os.path.join("reports", "Web")
    os.makedirs(reports_dir, exist_ok=True)
    config.option.htmlpath = os.path.join(reports_dir, f"Report-Web-{timestamp}.html")


SCREENSHOTS_DIR = os.path.join("reports", "screenshots", "web")
VIDEOS_DIR = os.path.join("reports", "videos", "web")

# Maps normalized test node IDs to TC numbers from TEST_CASES.md
TC_MAP = {
    # 1. Navigation
    "test_navigation.py::TestNavigation::test_nav_home_link":                                                       "TC1-1",
    "test_navigation.py::TestNavigation::test_nav_services_link":                                                   "TC1-2",
    "test_navigation.py::TestNavigation::test_nav_about_link":                                                      "TC1-3",
    "test_navigation.py::TestNavigation::test_nav_contact_link":                                                    "TC1-4",
    "test_navigation.py::TestNavigation::test_logo_navigates_home":                                                 "TC1-5",
    "test_navigation.py::TestNavigation::test_all_pages_load[/-https://replaceit.ai/]":                             "TC1-6",
    "test_navigation.py::TestNavigation::test_all_pages_load[/servicios-https://replaceit.ai/servicios]":           "TC1-7",
    "test_navigation.py::TestNavigation::test_all_pages_load[/quienes-somos-https://replaceit.ai/quienes-somos]":  "TC1-8",
    "test_navigation.py::TestNavigation::test_all_pages_load[/contacto-https://replaceit.ai/contacto]":            "TC1-9",
    # 2. Home Page
    "test_home.py::TestHomePage::test_hero_heading_visible":                                                        "TC2-1",
    "test_home.py::TestHomePage::test_clients_section_visible":                                                     "TC2-2",
    "test_home.py::TestHomePage::test_results_section_visible":                                                     "TC2-3",
    "test_home.py::TestHomePage::test_engagement_section_visible":                                                  "TC2-4",
    "test_home.py::TestHomePage::test_view_services_cta_navigates":                                                 "TC2-5",
    # 3. Services Page
    "test_services.py::TestServicesPage::test_hero_heading_visible":                                                "TC3-1",
    "test_services.py::TestServicesPage::test_all_service_cards_present":                                           "TC3-2",
    "test_services.py::TestServicesPage::test_service_card_count":                                                  "TC3-3",
    "test_services.py::TestServicesPage::test_apply_now_navigates_to_contact[0]":                                   "TC3-4",
    "test_services.py::TestServicesPage::test_apply_now_navigates_to_contact[1]":                                   "TC3-5",
    "test_services.py::TestServicesPage::test_apply_now_navigates_to_contact[2]":                                   "TC3-6",
    "test_services.py::TestServicesPage::test_apply_now_navigates_to_contact[3]":                                   "TC3-7",
    "test_services.py::TestServicesPage::test_apply_now_navigates_to_contact[4]":                                   "TC3-8",
    "test_services.py::TestServicesPage::test_apply_now_navigates_to_contact[5]":                                   "TC3-9",
    "test_services.py::TestServicesPage::test_apply_now_navigates_to_contact[6]":                                   "TC3-10",
    "test_services.py::TestServicesPage::test_apply_now_navigates_to_contact[7]":                                   "TC3-11",
    # 4. About Us Page
    "test_about.py::TestAboutPage::test_hero_heading_visible":                                                      "TC4-1",
    "test_about.py::TestAboutPage::test_gallery_section_visible":                                                   "TC4-2",
    # 5. Contact Page
    "test_contact.py::TestContactPage::test_hero_heading_visible":                                                  "TC5-1",
    "test_contact.py::TestContactPage::test_form_fields_present":                                                   "TC5-2",
    "test_contact.py::TestContactPage::test_send_button_present":                                                   "TC5-3",
    "test_contact.py::TestContactPage::test_contact_email_link_present":                                            "TC5-4",
    "test_contact.py::TestContactPage::test_phone_link_present":                                                    "TC5-5",
    "test_contact.py::TestContactPage::test_submit_empty_form_stays_on_page":                                       "TC5-6",
    "test_contact.py::TestContactPage::test_submit_with_invalid_email":                                             "TC5-7",
    "test_contact.py::TestContactPage::test_submit_valid_form":                                                     "TC5-8",
}


def _tc(nodeid: str) -> str:
    """Return the TC label for a test node ID, e.g. 'TC1-1'. Falls back to 'TCx'."""
    # nodeid may be prefixed with a directory, e.g. "tests/test_nav.py::..."
    normalized = nodeid.split("/")[-1]
    return TC_MAP.get(normalized, "TCx")


@pytest.fixture(scope="session")
def browser_context():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir=VIDEOS_DIR,
            record_video_size={"width": 1280, "height": 800},
        )
        yield context
        browser.close()


@pytest.fixture(scope="function")
def page(browser_context, request):
    page = browser_context.new_page()
    page.goto(os.getenv("BASE_URL", "https://replaceit.ai"))
    yield page

    # Grab video path before close() — close() finalizes the recording
    video_path = page.video.path() if page.video else None
    page.close()

    # Rename video using TC convention now that it is finalized
    if video_path:
        tc = _tc(request.node.nodeid)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        target = os.path.join(VIDEOS_DIR, f"REC-{tc}-{timestamp}.webm")
        try:
            page.video.save_as(target)
        except Exception:
            pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and "page" in item.funcargs:
        page = item.funcargs["page"]
        tc = _tc(item.nodeid)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        path = os.path.join(SCREENSHOTS_DIR, f"PIC-{tc}-{timestamp}.png")
        try:
            page.screenshot(path=path, full_page=True)
        except Exception:
            pass
