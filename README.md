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

---

## Telegram-Bot einrichten und aktivieren

Damit der Inserate-Monitor Nachrichten an dein Handy schicken kann, musst du einen eigenen Telegram-Bot einrichten.  
Das geht in wenigen Schritten:

1. **Bot erstellen**
   - Öffne Telegram und starte einen Chat mit [@BotFather](https://t.me/botfather).
   - Sende den Befehl `/newbot`.
   - Vergib einen Namen (z. B. `Auto Inserate Monitor`) und einen eindeutigen Benutzernamen (endet auf `_bot`).
   - Du erhältst ein **Bot Token**, z. B.:  
     ```
     123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
     ```

2. **Bot aktivieren**
   - Suche in Telegram deinen neuen Bot über den Benutzernamen.
   - Starte den Chat, indem du **"Start"** drückst oder `/start` sendest.  
     *Wichtig: Der Bot ist erst nach dieser Aktion aktiv und kann dir Nachrichten senden.*

3. **Chat-ID herausfinden**
   - Sende irgendeine Nachricht an deinen Bot (z. B. "Test").
   - Öffne im Browser:  
     ```
     https://api.telegram.org/botDEIN_BOT_TOKEN/getUpdates
     ```
   - In der JSON-Antwort findest du deine `chat.id`, z. B.:
     ```json
     {
       "update_id": 123456789,
       "message": {
         "chat": {
           "id": 987654321,
           "first_name": "Max",
           "type": "private"
         },
         "text": "Test"
       }
     }
     ```
   - In diesem Fall ist deine **CHAT_ID = 987654321**.

4. **Daten ins Script eintragen**
   - Öffne `monitor.py` und setze deine Werte ein:
     ```python
     BOT_TOKEN = "123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
     CHAT_ID = "987654321"
     ```

5. **Script starten**
   - Jetzt sendet der Monitor neue Inserate automatisch an deinen Telegram-Account.
