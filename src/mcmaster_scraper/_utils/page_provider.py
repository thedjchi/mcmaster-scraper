import asyncio
from playwright.async_api import async_playwright, Playwright, Browser, Page, BrowserContext

_browser: Browser | None = None
_browser_context: BrowserContext | None = None
_playwright: Playwright | None = None
_lock = asyncio.Lock()


async def _ensure_browser_context() -> BrowserContext:
    global _browser, _browser_context, _playwright

    async with _lock:
        if _browser_context:
            return _browser_context

        _playwright = await async_playwright().start()
        assert _playwright

        _browser = await _playwright.chromium.launch()
        assert _browser

        _browser_context = await _browser.new_context()
        assert _browser_context

        return _browser_context


async def get_page() -> Page:
    browser_context = await _ensure_browser_context()
    return await browser_context.new_page()
