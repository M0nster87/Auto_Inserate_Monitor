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
BOT_TOKEN = "8005136855:AAEY05CWz_7JVurx3GA-cabSsU5awHENdPU"  # von @BotFather
CHAT_ID = "-4894148454"


def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("Fehler beim Telegram-Senden:", response.text)
    except Exception as e:
        print("Fehler beim Telegram-Versand:", e)

# ====== JSON-Speicherort ======
json_path = os.path.join(os.path.dirname(__file__), "bmw_inserate.json")

# ====== Monitoring Loop ======
while True:
    try:
        # ChromeDriver automatisch installieren
        chromedriver_autoinstaller.install()

        # ====== Selenium Setup ======
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        # Chrome Logging unterdrücken
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=options)

        url = ("https://www.otomoto.pl/osobowe/bmw/od-2008?"
               "search%5Bfilter_enum_gearbox%5D=automatic&"
               "search%5Bfilter_float_engine_power%3Afrom%5D=170&"
               "search%5Bfilter_float_mileage%3Ato%5D=145000&"
               "search%5Bfilter_float_price%3Afrom%5D=4000&"
               "search%5Border%5D=relevance_web")
        driver.get(url)

        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article")))

        # ====== Inserate sammeln ======
        listings = driver.find_elements(By.CSS_SELECTOR, "article")
        cars = []

        for listing in listings:
            try:
                title = listing.find_element(By.CSS_SELECTOR, "h1, h2, h3").text.strip()
            except:
                title = "Kein Titel"
            try:
                link = listing.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except:
                link = "Kein Link"
            if "BMW" in title:
                cars.append({"title": title, "link": link})

        driver.quit()

        # ====== Alte Inserate laden ======
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                old_cars = json.load(f)
        except FileNotFoundError:
            old_cars = []

        old_links = {car['link'] for car in old_cars}
        fresh_cars = [car for car in cars if car['link'] not in old_links]

        # ====== Telegram nur für neue Inserate ======
        for car in fresh_cars:
            message = f"Neues BMW-Inserat:\n{car['title']}\n{car['link']}"
            send_telegram_message(BOT_TOKEN, CHAT_ID, message)
            print("Telegram gesendet:", car['title'])

        # ====== JSON aktualisieren ======
        updated_cars = old_cars + fresh_cars
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(updated_cars, f, ensure_ascii=False, indent=2)

        print(f"{len(fresh_cars)} neue BMW-Inserate gefunden, insgesamt {len(updated_cars)} gespeichert.", time.asctime())

    except Exception as e:
        print("Fehler im Monitoring-Lauf:", e)

    # ====== Intervall ======
    time.sleep(300)  # alle 5 Minuten prüfen
