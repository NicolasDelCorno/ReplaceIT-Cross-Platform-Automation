# Replace IT — Test Automation Suite

End-to-end test automation for [replaceit.ai](https://replaceit.ai), an AI services company. The suite covers the full public website across **web** (Playwright) and **mobile browsers** (Appium on iOS and Android), using the **Page Object Model** pattern throughout.

**34 test cases** across 5 areas: Navigation, Home, Services, About Us, and Contact.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3 |
| Web automation | Playwright + pytest-playwright |
| Mobile automation | Appium (XCUITest / UiAutomator2) |
| Test runner | pytest |
| Reporting | pytest-html (auto-generated HTML reports) |
| Evidence | Screenshots + video recording per test |

---

## Project Structure

```
replaceit/
├── pages/              # Web Page Objects (Playwright)
│   ├── base_page.py
│   ├── home_page.py
│   ├── about_page.py
│   ├── contact_page.py
│   └── services_page.py (implied by tests)
├── tests/              # Web test suite (Playwright)
│   ├── test_navigation.py
│   ├── test_home.py
│   ├── test_services.py
│   ├── test_about.py
│   └── test_contact.py
├── mobile/
│   ├── pages/          # Mobile Page Objects (Appium / Selenium)
│   └── tests/          # Mobile test suite (mirrors web suite)
├── ios/
│   └── conftest.py     # iOS-specific Appium fixture
├── reports/            # Auto-generated (gitignored)
│   ├── screenshots/
│   └── videos/
├── conftest.py         # Web fixtures: browser context, screenshots, video
├── mobile/conftest.py  # Mobile fixtures: Appium driver, platform selection
├── requirements.txt
├── .env.example
└── TEST_CASES.md       # Full test case catalogue
```

---

## Test Coverage

| # | Area | Tests |
|---|---|---|
| 1 | Navigation | 9 — nav links, logo, all pages load |
| 2 | Home Page | 5 — hero, sections visible, CTA navigation |
| 3 | Services Page | 11 — hero, 8 service cards, each "Apply now" link |
| 4 | About Us Page | 2 — hero, gallery section |
| 5 | Contact Page | 8 — form fields, validation, submission, contact details |

See [TEST_CASES.md](TEST_CASES.md) for the full catalogue with descriptions.

---

## Setup

### Prerequisites

- Python 3.10+
- For mobile tests: [Appium Server](https://appium.io) running locally on port 4723, plus the relevant simulator/emulator

### Install dependencies

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### Configure environment

```bash
cp .env.example .env
# Edit .env if you need to point at a different URL
```

---

## Running Tests

### Web (Playwright)

```bash
# All web tests
pytest tests/

# Single file
pytest tests/test_contact.py

# Headless mode
pytest tests/ --headed=false
```

### Mobile (Appium)

Start Appium Server first:
```bash
appium
```

Then run, selecting the target platform:

```bash
# iOS (default)
pytest mobile/tests/ --platform=ios

# Android
pytest mobile/tests/ --platform=android
```

> **Device configuration**: Update `device_name` and `platform_version` in `mobile/conftest.py` (or `ios/conftest.py` for iOS-only runs) to match your available simulator/emulator.

---

## Reports & Evidence

Each test run automatically generates:

- **HTML report** — timestamped, saved to `reports/Web/` or `reports/iOS|Android/`
- **Screenshots** — full-page capture after every test, named with TC number (e.g. `PIC-TC2-1-<timestamp>.png`)
- **Videos** — screen recordings for web tests, saved to `reports/videos/web/`

---

## Design Notes

- **Page Object Model** — all locators and interactions are encapsulated in page classes under `pages/` and `mobile/pages/`, keeping tests clean and locator changes contained to one place.
- **Shared mobile page objects** — the `ios/` suite reuses the page objects from `mobile/pages/` via a `sys.path` import, avoiding duplication.
- **TC mapping** — each test node ID is mapped to a numbered test case (TC1-1 through TC5-8) in `conftest.py`, so screenshots and videos are traceable back to the test catalogue.
- **Environment-driven base URL** — the target URL is read from `.env` (defaulting to `https://replaceit.ai`), making it easy to point tests at a staging environment.
