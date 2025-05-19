import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

PDF_DIR = Path("pdf_downloads")
URL_LIST_PATH = Path("pdf_urls.txt")
PDF_DIR.mkdir(exist_ok=True)

def get_filename_from_url(url):
    return url.strip().split("/")[-1]

async def download_pdf(context, url):
    filename = get_filename_from_url(url)
    output_path = PDF_DIR / filename

    if output_path.exists():
        print(f"[SKIP] Already downloaded: {filename}")
        return

    page = await context.new_page()

    try:
        print(f"[LOADING] {url}")
        await page.goto(url, timeout=20000)
        await page.wait_for_load_state("networkidle")

        link = await page.query_selector('a[href$=".pdf"]')
        if not link:
            print(f"[FAILED] No PDF link found on: {url}")
            await page.close()
            return

        with await context.expect_download() as download_info:
            await link.click()
        download = await download_info.value
        await download.save_as(str(output_path))
        print(f"[DOWNLOADED] {filename}")

    except Exception as e:
        print(f"[ERROR] {filename}: {e}")
    finally:
        await page.close()

async def main():
    if not URL_LIST_PATH.exists():
        print(f"[ERROR] File not found: {URL_LIST_PATH}")
        return

    with open(URL_LIST_PATH, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)

        for url in urls:
            await download_pdf(context, url)

        await context.close()
        await browser.close()

    print("[DONE] All downloads attempted.")

if __name__ == "__main__":
    asyncio.run(main())
