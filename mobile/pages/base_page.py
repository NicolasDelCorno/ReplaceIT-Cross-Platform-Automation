import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    SOCIAL_LINKS = {
        "instagram": "https://www.instagram.com/",
        "facebook": "https://www.facebook.com/",
        "linkedin": "https://www.linkedin.com/company/replaceit/",
    }

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_url(self, url):
        self.wait.until(EC.url_to_be(url))

    def current_url(self):
        return self.driver.current_url

    def get_h1(self):
        element = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1")))
        text = element.text.strip()
        if not text:
            text = (self.driver.execute_script("return arguments[0].innerText;", element) or "").strip()
        return text

    def scroll_to(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", element)
        try:
            self.wait.until(lambda d: d.execute_script(
                "var r = arguments[0].getBoundingClientRect(); "
                "return r.top < window.innerHeight && r.bottom > 0;",
                element,
            ))
        except Exception:
            pass

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def scroll_to_bottom(self):
        """Scroll incrementally to the bottom to trigger lazy-loaded content.
        Does NOT scroll back to top — caller is responsible if needed."""
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        step = 400
        pos = 0
        while pos < total_height:
            pos += step
            self.driver.execute_script(f"window.scrollTo(0, {pos});")
            time.sleep(0.3)
            total_height = self.driver.execute_script("return document.body.scrollHeight")

    # ── Footer ─────────────────────────────────────────────────────────────────

    def get_footer_link(self, href):
        self.scroll_to_bottom()
        return self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"footer a[href='{href}']"))
        )

    def click_privacy_policy(self):
        self.scroll_to_bottom()
        link = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='#priv']")))
        self.js_click(link)

    def click_cookie_policy(self):
        self.scroll_to_bottom()
        link = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='#cookies']")))
        self.js_click(link)

    def click_terms_and_conditions(self):
        self.scroll_to_bottom()
        link = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='#term']")))
        self.js_click(link)

    # ── Navigation ─────────────────────────────────────────────────────────────

    def _open_nav_menu(self):
        """Try to open the hamburger menu on mobile. Falls back silently."""
        selectors = [
            "button[aria-label='Open menu']",
            "button[aria-label='Toggle menu']",
            "button[aria-label='menu']",
            "button[aria-label='Menu']",
            "button.hamburger",
            ".menu-toggle",
            "[class*='hamburger']",
            "[class*='Hamburger']",
            "[class*='burger']",
            "header button",
        ]
        for sel in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, sel)
                for btn in elements:
                    if btn.is_displayed():
                        self.js_click(btn)
                        time.sleep(0.5)
                        return
            except Exception:
                continue

    def _click_nav_link(self, href):
        """Open the nav menu then JS-click the link (bypasses interactability)."""
        self._open_nav_menu()
        link = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"header a[href='{href}']"))
        )
        self.js_click(link)

    def click_nav_home(self):
        self._click_nav_link("/")

    def click_nav_services(self):
        self._click_nav_link("/servicios")

    def click_nav_about(self):
        self._click_nav_link("/quienes-somos")

    def click_nav_contact(self):
        self._click_nav_link("/contacto")

    def click_logo(self):
        link = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "header a[href='/']"))
        )
        self.js_click(link)
