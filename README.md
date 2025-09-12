# BMW & Audi Inserate Monitor

### Projektbeschreibung
Dieses Tool überwacht automatisch neue Inserate für BMW und Audi auf [otomoto.pl](https://www.otomoto.pl/) anhand vordefinierter Kriterien 
(Baujahr ab 2008, Automatikgetriebe, mind. 190 PS, max. 750.000 Pln Preis). 
Neue Inserate werden über einen Telegram-Bot gemeldet und lokal in einer JSON-Datei gespeichert.

---

## Features
- Automatisches Monitoring alle 5 Minuten
- Benachrichtigung über neue Inserate per Telegram-Bot
- Historie der Inserate in `bmw_inserate.json` gespeichert
- Einfache Erweiterung für zusätzliche Filter oder Plattformen

---

## Voraussetzungen
- Python 3.x
- Google Chrome installiert
- Telegram-Bot (Token von @BotFather)
- Chat-ID für Benachrichtigungen

---

## Installation
- git clone https://github.com/M0nster87/Bmw_inserate_Monitor.git
- cd Bmw_inserate_Monitor
- pip install -r requirements.txt
