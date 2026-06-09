import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    if not os.path.exists("assets"):
        os.makedirs("assets")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        print("Capturing MLflow...")
        try:
            await page.goto('http://127.0.0.1:5000', wait_until='domcontentloaded')
            await page.wait_for_timeout(3000)
            await page.screenshot(path='assets/mlflow_dashboard.png')
            print("MLflow screenshot saved.")
        except Exception as e:
            print(f"Error capturing MLflow: {e}")

        print("Capturing ZenML...")
        try:
            await page.goto('http://127.0.0.1:8237/pipelines', wait_until='networkidle')
            await page.wait_for_timeout(5000)
            await page.screenshot(path='assets/zenml_dashboard.png')
            print("ZenML screenshot saved.")
        except Exception as e:
            print(f"Error capturing ZenML: {e}")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
