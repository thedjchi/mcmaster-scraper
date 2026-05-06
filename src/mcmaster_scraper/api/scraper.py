from playwright.async_api import async_playwright, Response
import json


# TODO input validation (valid McMaster url)
# TODO handle no product page
# TODO handle other errors
async def get_product_api_response(url: str) -> dict:
    # Using Playwright because the API
    async with async_playwright() as pw:
        print("Finding API for product page...")
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url)

        # If the JSON is too large, the response will be evicted from the inspector cache before we can access it
        # As a workaround, we can navigate to the API URL and extract the response from the page's body
        product_api = "**/ProdPageWebPart.aspx?**"
        async with page.expect_request(product_api) as request:
            value = await request.value
            api_url = value.url

        print("Getting API response...")
        await page.goto(api_url)

        res = await page.locator('body').text_content()
        assert res is not None

        data = _extract_json_from_response(res)

        await browser.close()
        return data


def _extract_json_from_response(res: str) -> dict:
    start = res.find("{")
    end = res.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON found in API response")

    json_str = res[start:end + 1]
    return json.loads(json_str)
