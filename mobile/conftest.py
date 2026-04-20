import os
import pytest
import json
from datetime import datetime
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.options.ios.xcuitest.base import XCUITestOptions
from dotenv import load_dotenv

load_dotenv()

APPIUM_SERVER = "http://127.0.0.1:4723"


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://replaceit.ai").rstrip("/")

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
}


def _tc(nodeid: str) -> str:
    """Return the TC label for a test node ID, e.g. 'TC1-1'. Falls back to 'TCx'."""
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
        "suite": "mobile",
        "run_started_at": getattr(config, "_run_started_at", None),
        "exitstatus": exitstatus,
        "base_url": os.getenv("BASE_URL", "https://replaceit.ai").rstrip("/"),
        "platform": config.getoption("--platform", default="ios"),
        "failures": getattr(config, "_failures", []),
    }

    try:
        root_path = os.path.join(os.path.dirname(__file__), "..", "failures.json")
        with open(root_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def pytest_configure(config):
    try:
        platform = config.getoption("--platform")
    except ValueError:
        platform = "ios"
    platform_label = "iOS" if platform == "ios" else "Android"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports", platform_label)
    os.makedirs(reports_dir, exist_ok=True)
    config.option.htmlpath = os.path.join(reports_dir, f"Report-{platform_label}-{timestamp}.html")
    # Session-level failure collector written at the end of the run.
    config._failures = []
    config._run_started_at = timestamp


def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default="ios",
        choices=["ios", "android"],
        help="Mobile platform: ios or android",
    )


def _ios_options():
    opts = XCUITestOptions()
    opts.platform_name = "iOS"
    opts.automation_name = "XCUITest"
    opts.device_name = "iPhone 17"     # adjust to your available simulator name
    opts.platform_version = "26.1"    # adjust to match simulator OS version
    opts.browser_name = "Safari"
    return opts


def _android_options():
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.automation_name = "UiAutomator2"
    opts.device_name = "emulator-5554"  # adjust to your AVD name
    opts.browser_name = "Chrome"
    opts.set_capability("appium:chromedriverAutodownload", True)
    return opts


@pytest.fixture(scope="session")
def driver(request):
    platform = request.config.getoption("--platform")
    options = _ios_options() if platform == "ios" else _android_options()
    screenshots_dir = os.path.join(
        os.path.dirname(__file__), "..", "reports", "screenshots", platform
    )
    os.makedirs(screenshots_dir, exist_ok=True)
    request.config._mobile_screenshots_dir = screenshots_dir
    drv = webdriver.Remote(APPIUM_SERVER, options=options)
    yield drv
    drv.quit()


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
            "platform": config.getoption("--platform", default="ios"),
        }
        try:
            config._failures.append(entry)
        except Exception:
            pass

    if report.when == "call" and "driver" in item.funcargs:
        driver = item.funcargs["driver"]
        tc = _tc(item.nodeid)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        screenshots_dir = getattr(item.config, "_mobile_screenshots_dir", "reports/screenshots")
        path = os.path.join(screenshots_dir, f"PIC-{tc}-{timestamp}.png")
        try:
            driver.get_screenshot_as_file(path)
        except Exception:
            pass
