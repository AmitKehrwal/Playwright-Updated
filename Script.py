import time
import threading
import warnings
from faker import Faker
from playwright.sync_api import sync_playwright

warnings.filterwarnings('ignore')
fake = Faker('en_IN')
MUTEX = threading.Lock()

def sync_print(text):
    with MUTEX:
        print(text)

def start(name, proxy, user, wait_time, meetingcode, passcode):
    sync_print(f"{name} started!")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto(f'https://zoom.us/wc/join/{meetingcode}')
            time.sleep(10)

            inp = page.locator('//input[@type="text"]')
            inp.fill(f"{user}")
            time.sleep(5)

            inp2 = page.locator('//input[@type="password"]')
            inp2.fill(passcode)

            # Click the "Join" button
            join_button = page.locator('//button[contains(@class,"preview-join-button")]')
            join_button.click()

            sync_print(f"{name} sleep for {wait_time} seconds ...")
            time.sleep(wait_time)
            sync_print(f"{name} ended!")

        finally:
            context.close()

def main():
    number = 5
    meetingcode = "82770760919"
    passcode = "468111"
    sec = 60
    wait_time = sec * 60
    workers = []

    for i in range(number):
        try:
            proxy = proxylist[i]
        except Exception:
            proxy = None
        try:
            user = fake.name()
        except IndexError:
            break
        wk = threading.Thread(target=start, args=(
            f'[Thread{i}]', proxy, user, wait_time, meetingcode, passcode))
        workers.append(wk)

    for wk in workers:
        wk.start()

    for wk in workers:
        wk.join()

if __name__ == '__main__':
    try:
        main()
    except:
        pass
