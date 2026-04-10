import sys
import os

# Make mobile/pages importable from the shared mobile directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mobile'))

import pytest
from appium import webdriver
from appium.options.ios.xcuitest.base import XCUITestOptions

APPIUM_SERVER = "http://127.0.0.1:4723"


def _ios_options():
    opts = XCUITestOptions()
    opts.platform_name = "iOS"
    opts.automation_name = "XCUITest"
    opts.device_name = "iPhone 17"      # adjust to your available simulator name
    opts.platform_version = "26.1"      # adjust to match simulator OS version
    opts.browser_name = "Safari"
    return opts


@pytest.fixture(scope="session")
def driver():
    drv = webdriver.Remote(APPIUM_SERVER, options=_ios_options())
    yield drv
    drv.quit()
