# Future Imports
from __future__ import annotations

# Standard Library Imports
import asyncio
import io

import pyppeteer

# Dependency Imports
from pyppeteer import launch


async def screenshot(self, ctx, link: str, wait: int = 3):
    """
    Screenshots a given link.
    If no time is given, it will wait 3 seconds to screenshot
    """
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({"width": 1280, "height": 720})
    try:
        await page.goto(link)
    except pyppeteer.page.PageError:
        await browser.close()
        return
    except Exception:
        await browser.close()
        return

    await asyncio.sleep(wait)
    result = await page.screenshot()
    await browser.close()
    f = io.BytesIO(result)
    return f
