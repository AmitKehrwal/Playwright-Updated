import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
import nest_asyncio
import random
import getindianname as name

nest_asyncio.apply()

# Event to signal when the microphone is activated
mic_activated_event = asyncio.Event()

# Flag to indicate whether the script is running
running = True

async def start(name, user, wait_time, meetingcode, passcode):
    print(f"{name} started!")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream'])
        context = await browser.new_context(permissions=['microphone'])
        page = await context.new_page()
        await page.goto(f'http://app.zoom.us/wc/join/{meetingcode}', timeout=200000)

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
            query = '//button[text()="Join Audio by Computer"]'
            await asyncio.sleep(13)
            mic_button_locator = await page.wait_for_selector(query, timeout=370000)
            await asyncio.sleep(10)
            await mic_button_locator.evaluate_handle('node => node.click()')
            print(f"{name} mic aayenge.")
            
            # Signal that the microphone is activated
            mic_activated_event.set()

        except Exception as e:
            print(f"{name} mic nahe aayenge. ", e)

        print(f"{name} sleep for {wait_time} seconds ...")
        while running and wait_time > 0:
            await asyncio.sleep(1)
            wait_time -= 1
        print(f"{name} ended!")

        await browser.close()

def start_thread(user, wait_time, meetingcode, passcode):
    thread = threading.Thread(target=asyncio.run, args=(start(f'[Thread]', user, wait_time, meetingcode, passcode),))
    thread.start()
    return thread

async def main():
    global running
    meetingcode = input("Enter meeting code (No Space): ")
    passcode = input("Enter Password (No Space): ")

    sec = 90
    wait_time = sec * 60

    try:
        num_threads = int(input("Enter the number of threads to start: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    for _ in range(num_threads):
        try:
            user = name.randname()
        except IndexError:
            break
        start_thread(user, wait_time, meetingcode, passcode)

        # Wait for microphone activation event before starting the next thread
        await mic_activated_event.wait()
        mic_activated_event.clear()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        running = False
