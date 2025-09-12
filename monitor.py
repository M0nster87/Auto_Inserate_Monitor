import json
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

# ====== Telegram Einstellungen ======
BOT_TOKEN = "HIER_DEIN_BOT_TOKEN"
CHAT_ID = "HIER_DEINE_CHAT_ID"

def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("Fehler beim Telegram-Senden:", response.text)
    except Exception as e:
        print("Fehler beim Telegram-Versand:", e)

# ====== JSON Handling ======
json_path = os.path.join(os.path.expanduser(r"C:\Users\PH\Documents"), "autos_inserate.json")

def load_json_safe(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        print("Warnung: JSON beschädigt, starte mit leerer Liste")
        return []

# ====== Markenliste ======
brands = ["BMW", "Audi"]

# ====== Monitoring Loop ======
while True:
    try:
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)

        old_cars = load_json_safe(json_path)
        old_links = {car['link'] for car in old_cars}
        fresh_cars = []

        for brand in brands:
            url = (
                f"https://www.otomoto.pl/osobowe/{brand.lower()}/od-2008?"
                "search%5Bfilter_enum_gearbox%5D=automatic&"
                "search%5Bfilter_float_engine_power%3Afrom%5D=190&"
                "search%5Bfilter_float_price%3Ato%5D=750000&"
                "search%5Border%5D=relevance_web"
            )
            driver.get(url)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article")))

            listings = driver.find_elements(By.CSS_SELECTOR, "article")

            for listing in listings:
                try:
                    title = listing.find_element(By.CSS_SELECTOR, "h1, h2, h3").text.strip()
                except:
                    title = "Kein Titel"
                try:
                    link = listing.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                except:
                    link = "Kein Link"

                if brand in title and link not in old_links:
                    car_data = {"brand": brand, "title": title, "link": link}
                    fresh_cars.append(car_data)
                    old_links.add(link)

        driver.quit()

        # Telegram senden
        for car in fresh_cars:
            message = f"Neues {car['brand']}-Inserat:\n{car['title']}\n{car['link']}"
            send_telegram_message(BOT_TOKEN, CHAT_ID, message)
            print("Telegram gesendet:", car['title'])

        # JSON aktualisieren
        updated_cars = old_cars + fresh_cars
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(updated_cars, f, ensure_ascii=False, indent=2)

        print(f"{len(fresh_cars)} neue Inserate gefunden, insgesamt {len(updated_cars)} gespeichert.", time.asctime())

    except Exception as e:
        print("Fehler im Monitoring-Lauf:", e)

    time.sleep(300)  # 5 Minuten warten
