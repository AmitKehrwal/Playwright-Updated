import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
import nest_asyncio
import random
import getindianname as name

nest_asyncio.apply()

# Flag to indicate whether the script is running
running = True

# Lock to make the print statements thread-safe
print_lock = threading.Lock()

async def start(user, wait_time, meetingcode, passcode):
    with print_lock:
        print(f"{user} joined.")

    async with async_playwright() as p:
        browser = await p.firefox.launch(
            headless=True,
            args=['--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream']
        )
        context = await browser.new_context()

        page = await context.new_page()
        await page.goto(f'http://app.zoom.us/wc/join/{meetingcode}', timeout=200000)

        # Explicitly request microphone permission using JavaScript multiple times
        for _ in range(5):
            await page.evaluate('() => { navigator.mediaDevices.getUserMedia({ audio: true }); }')

        try:
            await page.click('//button[@id="onetrust-accept-btn-handler"]', timeout=5000)
        except Exception as e:
            pass

        try:
            await page.click('//button[@id="wc_agree1"]', timeout=5000)
        except Exception as e:
            pass

        try:
            await page.wait_for_selector('input[type="text"]', timeout=200000)
            await page.fill('input[type="text"]', user)
            await page.fill('input[type="password"]', passcode)
            join_button = await page.wait_for_selector('button.preview-join-button', timeout=200000)
            await join_button.click()
        except Exception as e:
            pass

        try:
            await page.wait_for_selector('button.join-audio-by-voip__join-btn', timeout=300000)
            query = 'button[class*="join-audio-by-voip__join-btn"]'
            mic_button_locator = await page.query_selector(query)
            await asyncio.sleep(5)
            await mic_button_locator.evaluate_handle('node => node.click()')
            print(f"{name} mic aayenge.")
        except Exception as e:
            print(f"{name} mic nahe aayenge. ", e)

        print(f"{user} sleep for {wait_time} seconds ...")
        while running and wait_time > 0:
            await asyncio.sleep(1)
            wait_time -= 1
        print(f"{user} ended!")

    # Close the context and browser outside of the async with block
    await context.close()
    await browser.close()

async def main():
    global running
    number = 5
    meetingcode = "82770760919"
    passcode = "468111"

    sec = 90
    wait_time = sec * 80

    with ThreadPoolExecutor(max_workers=number) as executor:
        loop = asyncio.get_running_loop()
        tasks = []
        for i in range(number):
            try:
                # Generate a random Indian name using getindianname
                user = name.randname()
            except IndexError:
                break
            task = loop.create_task(start(user, wait_time, meetingcode, passcode))
            tasks.append(task)

    try:
        await asyncio.gather(*tasks, return_exceptions=True)
    except KeyboardInterrupt:
        running = False
        # Wait for tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
