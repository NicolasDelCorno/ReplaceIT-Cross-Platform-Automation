import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


EXPECTED_SERVICES_IOS = [
    "Autonomous AI Agents",
    "Chatbots with RAG",
    "Computer Vision",
    "Process Automation",
    "Generative AI",
    "Recommendation Systems",
    "NLP & Sentiment Analysis",
]

EXPECTED_SERVICES_ANDROID = [
    "Chatbots with RAG",
    "Autonomous AI Agents",
    "Computer Vision",
    "Process Automation",
    "Generative AI",
    "NLP & Sentiment Analysis",
    "Recommendation Systems",
    "Document Processing",
]

# Default used when platform is not specified
EXPECTED_SERVICES = EXPECTED_SERVICES_IOS


class ServicesPage(BasePage):
    def get_hero_heading(self):
        return self.get_h1()

    def _collect_all_headings_and_links(self):
        """
        Scroll slowly through the page collecting all h3 texts and apply-now
        links as they appear. Returns (headings_set, links_list).
        Works even if the page uses virtual scrolling (cards unload off-screen).
        """
        headings = set()
        links = []
        seen_link_hrefs = set()

        total_height = self.driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
        step = 400
        pos = 0

        while pos <= total_height + step:
            self.driver.execute_script(f"window.scrollTo(0, {pos});")
            time.sleep(0.3)

            for el in self.driver.find_elements(By.CSS_SELECTOR, "h3"):
                txt = el.text.strip()
                if txt:
                    headings.add(txt)

            for el in self.driver.find_elements(By.CSS_SELECTOR, "a[href='/contacto']"):
                if "Apply now" in el.text:
                    try:
                        key = self.driver.execute_script("""
                            var el = arguments[0], p = el.parentElement;
                            while (p) {
                                var h3 = p.querySelector('h3');
                                if (h3) return h3.textContent.trim();
                                p = p.parentElement;
                            }
                            return null;
                        """, el)
                    except Exception:
                        key = None
                    if key and key not in seen_link_hrefs:
                        seen_link_hrefs.add(key)
                        links.append(el)

            pos += step
            total_height = self.driver.execute_script(
                "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")

        return headings, links

    def get_service_headings(self):
        headings, _ = self._collect_all_headings_and_links()
        return list(headings)

    def get_apply_now_links(self):
        _, links = self._collect_all_headings_and_links()
        return links

    def click_apply_now(self, index=0):
        # Re-scroll to find the specific link fresh (stale element risk after full scroll)
        total_height = self.driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
        step = 400
        pos = 0
        count = 0

        while pos <= total_height + step:
            self.driver.execute_script(f"window.scrollTo(0, {pos});")
            time.sleep(0.3)

            for el in self.driver.find_elements(By.CSS_SELECTOR, "a[href='/contacto']"):
                if "Apply now" in el.text:
                    if count == index:
                        self.js_click(el)
                        return
                    count += 1

            pos += step
            total_height = self.driver.execute_script(
                "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")

        raise IndexError(f"Apply now link at index {index} not found")
