import time
import json
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

# ====== Telegram-Konfiguration ======
BOT_TOKEN = ""
CHAT_ID = ""

# ====== Filter-Parameter ======
MIN_PS = 190
MAX_KM = 150000
BAUJAHR_AB = 2008
MAX_PREIS_PLN = 75000
brands = ["BMW", "Audi"]

# ====== JSON-Datei für bekannte Inserate ======
SEEN_FILE = "seen.json"

def load_seen():
    try:
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, indent=2, ensure_ascii=False)

# ====== Telegram Nachricht senden ======
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "disable_web_page_preview": True}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Fehler beim Senden an Telegram:", e)

# ====== Scraper ======
def scrape_otomoto(old_links):
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")        # unsichtbar
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    fresh_cars = []

    try:
        url = (
            f"https://www.otomoto.pl/osobowe/audi--bmw/od-{BAUJAHR_AB}?"
            f"search%5Bfilter_enum_gearbox%5D=automatic&"
            f"search%5Bfilter_float_engine_power%3Afrom%5D={MIN_PS}&"
            f"search%5Bfilter_float_mileage%3Ato%5D={MAX_KM}&"
            f"search%5Bfilter_float_price%3Ato%5D={MAX_PREIS_PLN}&"
            f"search%5Border%5D=created_at_first%3Adesc"
        )

        driver.get(url)

        # Warten, bis Artikel geladen sind (max. 30s)
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article")))

        listings = driver.find_elements(By.CSS_SELECTOR, "article")

        for listing in listings:
            try:
                title = listing.find_element(By.CSS_SELECTOR, "h1, h2, h3").text.strip()
                link = listing.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                if link and link not in old_links:
                    fresh_cars.append({"title": title, "link": link})
            except:
                continue
    finally:
        driver.quit()  # Browser direkt schließen

    return fresh_cars

# ====== Main Loop ======
if __name__ == "__main__":
    seen_links = load_seen()

    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{timestamp}] Neuer Durchlauf gestartet...")

            try:
                fresh = scrape_otomoto(seen_links)
            except Exception as e:
                print(f"[{timestamp}] Fehler beim Scraping: {e}")
                fresh = []

            if fresh:
                print(f"[{timestamp}] {len(fresh)} neue Inserate gefunden!")
                for car in fresh:
                    msg = f"{car['title']}\n{car['link']}"
                    print(f"- {car['title']} | {car['link']}")
                    send_telegram(msg)
                    seen_links.add(car['link'])
                save_seen(seen_links)
            else:
                print(f"[{timestamp}] Keine neuen Inserate gefunden.")

            time.sleep(600)  # 10 Minuten warten
    except KeyboardInterrupt:
        print("Beendet durch Benutzer.")
