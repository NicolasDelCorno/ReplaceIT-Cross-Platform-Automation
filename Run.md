# Running the Replace IT automation suites

This repo contains:
- **Web suite**: Playwright + pytest (`tests/`)
- **Mobile browser suite**: Appium + pytest (`mobile/tests/`) for **iOS Safari** / **Android Chrome**

---

## 0) One-time setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env
```

---

## 1) Configure target environment (optional)

Edit `.env`:

```bash
# Example
BASE_URL=https://replaceit.ai
```

---

## 2) Web (Playwright) suite

### Run all web tests (headed)

```bash
./venv/bin/python -m pytest tests/
```

### Run all web tests (headless)

```bash
HEADLESS=1 ./venv/bin/python -m pytest tests/
```

### Run a single web file

```bash
HEADLESS=1 ./venv/bin/python -m pytest tests/test_contact.py
```

### Run a single web test (parametrized IDs need quotes in zsh)

```bash
HEADLESS=1 ./venv/bin/python -m pytest "tests/test_navigation.py::TestNavigation::test_all_pages_load[/]"
```

### Cross-browser smoke (web)

Your custom Playwright engine flag is `--pw-browser`:

```bash
HEADLESS=1 ./venv/bin/python -m pytest tests/test_quality_gates.py --pw-browser=chromium
HEADLESS=1 ./venv/bin/python -m pytest tests/test_quality_gates.py --pw-browser=firefox
HEADLESS=1 ./venv/bin/python -m pytest tests/test_quality_gates.py --pw-browser=webkit
```

---

## 3) Mobile browser suite (Appium)

### Start Appium server (in a separate terminal)

```bash
appium
```

### Run all mobile tests on iOS Safari

```bash
./venv/bin/python -m pytest mobile/tests/ --platform=ios
```

### Run all mobile tests on Android Chrome

```bash
./venv/bin/python -m pytest mobile/tests/ --platform=android
```

### Run a single mobile test file

```bash
./venv/bin/python -m pytest mobile/tests/test_contact.py --platform=ios
```

---

## 4) Reports & evidence output

- **Web HTML report**: `reports/Web/Report-Web-<timestamp>.html`
- **Web screenshots**: `reports/screenshots/web/`
- **Web videos**: `reports/videos/web/`
- **Mobile HTML report**: `reports/iOS/` or `reports/Android/`
- **Mobile screenshots**: `reports/screenshots/ios/` or `reports/screenshots/android/`

