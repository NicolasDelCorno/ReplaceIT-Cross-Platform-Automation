import pytest


@pytest.mark.ui
class TestQualityGates:
    @pytest.mark.parametrize("path", ["/", "/servicios", "/quienes-somos", "/contacto"])
    def test_no_severe_console_errors_on_load(self, page, base_url, path):
        console_errors = []
        page_errors = []

        def on_console(msg):
            if msg.type == "error":
                console_errors.append(msg.text)

        def on_page_error(err):
            page_errors.append(str(err))

        page.on("console", on_console)
        page.on("pageerror", on_page_error)

        page.goto(f"{base_url}{path}", wait_until="networkidle")
        assert page.locator("h1").first.is_visible()

        assert page_errors == []
        assert console_errors == []

    def test_unknown_route_has_expected_behavior(self, page, base_url):
        response = page.goto(f"{base_url}/does-not-exist-qa", wait_until="networkidle")

        # Accept either a real 404 or a redirect to home (some static hosts do that).
        if response and response.status == 404:
            assert page.locator("text=404").first.is_visible() or page.locator("text=Not Found").first.is_visible()
        else:
            assert page.url in (f"{base_url}/", f"{base_url}/does-not-exist-qa")
            assert page.locator("h1").first.is_visible()
