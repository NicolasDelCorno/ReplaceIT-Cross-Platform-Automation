from playwright.sync_api import sync_playwright

PAGES = [
    ("Home", "/"),
    ("Services", "/servicios"),
    ("About Us", "/quienes-somos"),
    ("Contact", "/contacto"),
]

def explore_page(page, path, label):
    page.goto(f"https://replaceit.ai{path}", wait_until="networkidle")
    print(f"\n{'='*50}")
    print(f"PAGE: {label} ({path})")
    print(f"{'='*50}")

    print("HEADINGS:")
    for h in page.locator("h1, h2, h3").all()[:15]:
        text = h.inner_text().strip()
        if text:
            tag = h.evaluate("el => el.tagName")
            print(f"  <{tag}> {text}")

    print("BUTTONS:")
    for btn in page.locator("button, a[role='button'], [class*='btn']").all()[:15]:
        text = btn.inner_text().strip()
        if text:
            print(f"  [{text}]")

    print("FORMS:")
    forms = page.locator("form").all()
    print(f"  {len(forms)} form(s)")
    for i, form in enumerate(forms):
        inputs = form.locator("input, textarea, select").all()
        print(f"  Form {i+1}: {len(inputs)} field(s)")
        for inp in inputs:
            print(f"    - type={inp.get_attribute('type')} | name={inp.get_attribute('name')} | placeholder={inp.get_attribute('placeholder')}")

    print("LINKS:")
    for link in page.locator("a[href]").all():
        href = link.get_attribute("href")
        text = link.inner_text().strip()
        if href:
            print(f"  {text or '(no text)'} -> {href}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        pg = browser.new_page(viewport={"width": 1280, "height": 800})
        for label, path in PAGES:
            explore_page(pg, path, label)
        browser.close()

if __name__ == "__main__":
    main()
