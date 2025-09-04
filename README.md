# BMW Inserate Monitor

## Projektbeschreibung
Dieses Python-Projekt überwacht BMW-Inserate auf [Otomoto.pl](https://www.otomoto.pl/) und benachrichtigt Sie automatisch über neue Inserate via Telegram. Bereits gefundene Inserate werden in einer JSON-Datei gespeichert, um Doppelbenachrichtigungen zu vermeiden.


### Überwachungs-Kriterien
- Baujahr ab 2008
- Automatikgetriebe
- Mindestens 170 PS
- Preis ab 4000 €
- Max. 145.000 km Laufleistung

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
1. Repository klonen:
```bash
git clone https://github.com/M0nster87/Bmw_inserate_Monitor.git
cd Bmw_inserate_Monitor
