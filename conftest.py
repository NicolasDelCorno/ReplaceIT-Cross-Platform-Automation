import os
import pytest
import json
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://replaceit.ai").rstrip("/")


def pytest_addoption(parser):
    parser.addoption(
        "--pw-browser",
        action="store",
        default=os.getenv("BROWSER", "chromium"),
        choices=["chromium", "firefox", "webkit"],
        help="Playwright browser engine to run (custom fixture): chromium, firefox, or webkit",
    )


def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    reports_dir = os.path.join("reports", "Web")
    os.makedirs(reports_dir, exist_ok=True)
    config.option.htmlpath = os.path.join(reports_dir, f"Report-Web-{timestamp}.html")
    # Session-level failure collector written at the end of the run.
    config._failures = []
    config._run_started_at = timestamp


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
    "test_navigation.py::TestNavigation::test_all_pages_load[/]":                                                   "TC1-6",
    "test_navigation.py::TestNavigation::test_all_pages_load[/servicios]":                                          "TC1-7",
    "test_navigation.py::TestNavigation::test_all_pages_load[/quienes-somos]":                                     "TC1-8",
    "test_navigation.py::TestNavigation::test_all_pages_load[/contacto]":                                           "TC1-9",
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
    # 6. Footer & Compliance
    "test_footer.py::TestFooter::test_privacy_policy_link_works":                                                   "TC6-1",
    "test_footer.py::TestFooter::test_cookie_policy_link_works":                                                    "TC6-2",
    "test_footer.py::TestFooter::test_terms_and_conditions_link_works":                                             "TC6-3",
    "test_footer.py::TestFooter::test_social_links_present_in_footer[instagram]":                                   "TC6-4",
    "test_footer.py::TestFooter::test_social_links_present_in_footer[facebook]":                                    "TC6-5",
    "test_footer.py::TestFooter::test_social_links_present_in_footer[linkedin]":                                    "TC6-6",
    # 7. Cross-cutting (Quality Gates)
    "test_quality_gates.py::TestQualityGates::test_no_severe_console_errors_on_load[/]":                            "TC7-1",
    "test_quality_gates.py::TestQualityGates::test_no_severe_console_errors_on_load[/servicios]":                   "TC7-2",
    "test_quality_gates.py::TestQualityGates::test_no_severe_console_errors_on_load[/quienes-somos]":              "TC7-3",
    "test_quality_gates.py::TestQualityGates::test_no_severe_console_errors_on_load[/contacto]":                   "TC7-4",
    "test_quality_gates.py::TestQualityGates::test_unknown_route_has_expected_behavior":                            "TC7-5",
}


def _tc(nodeid: str) -> str:
    """Return the TC label for a test node ID, e.g. 'TC1-1'. Falls back to 'TCx'."""
    # nodeid may be prefixed with a directory, e.g. "tests/test_nav.py::..."
    normalized = nodeid.split("/")[-1]
    return TC_MAP.get(normalized, "TCx")


def _safe_longrepr(report) -> str:
    try:
        return report.longreprtext
    except Exception:
        try:
            return str(report.longrepr)
        except Exception:
            return ""

def pytest_sessionfinish(session, exitstatus):
    config = session.config
    payload = {
        "schema_version": 1,
        "suite": "web",
        "run_started_at": getattr(config, "_run_started_at", None),
        "exitstatus": exitstatus,
        "base_url": os.getenv("BASE_URL", "https://replaceit.ai").rstrip("/"),
        "pw_browser": config.getoption("--pw-browser"),
        "headless": os.getenv("HEADLESS", "false").strip().lower() in ("1", "true", "yes", "y"),
        "failures": getattr(config, "_failures", []),
    }

    # Write at repo root for easy pickup by humans/agents.
    try:
        with open("failures.json", "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


@pytest.fixture(scope="session")
def browser_context(request):
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    with sync_playwright() as p:
        browser_name = request.config.getoption("--pw-browser")
        headless_env = os.getenv("HEADLESS", "false").strip().lower()
        headless = headless_env in ("1", "true", "yes", "y")
        browser = getattr(p, browser_name).launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir=VIDEOS_DIR,
            record_video_size={"width": 1280, "height": 800},
        )
        yield context
        browser.close()


@pytest.fixture(scope="function")
def page(browser_context, request, base_url):
    page = browser_context.new_page()
    page.goto(base_url)
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

    # Record failures/errors into failures.json (covers setup/call/teardown)
    if report.failed:
        config = item.config
        nodeid = report.nodeid
        tc = _tc(nodeid)
        started_at = getattr(config, "_run_started_at", None)
        entry = {
            "nodeid": nodeid,
            "tc": tc,
            "when": report.when,
            "outcome": report.outcome,
            "message": getattr(report, "longreprcrash", None).message if getattr(report, "longreprcrash", None) else None,
            "longrepr": _safe_longrepr(report),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "run_started_at": started_at,
            "base_url": os.getenv("BASE_URL", "https://replaceit.ai").rstrip("/"),
            "pw_browser": config.getoption("--pw-browser"),
            "headless": os.getenv("HEADLESS", "false").strip().lower() in ("1", "true", "yes", "y"),
        }
        try:
            config._failures.append(entry)
        except Exception:
            pass

    if report.when == "call" and "page" in item.funcargs:
        page = item.funcargs["page"]
        tc = _tc(item.nodeid)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        path = os.path.join(SCREENSHOTS_DIR, f"PIC-{tc}-{timestamp}.png")
        try:
            page.screenshot(path=path, full_page=True)
        except Exception:
            pass
