import asyncio
from typing import Union

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)

_browser: Union[Browser, None] = None
_browser_context: Union[BrowserContext, None] = None
_playwright: Union[Playwright, None] = None
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
