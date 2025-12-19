# Labration 1 - API Automation
 
Detta verktyg automatiserar processen att hämta, verifiera och skicka data i ett flerstegs-API för att hämta en flagga.
 
## Krav

- Python 3.x

- `requests` biblioteket
 
## Installation
 
1. Klona repot:

   ```bash

   git clone https://github.com/edgbou/Python_projects.git

   cd Laborationer

   ```
 
2. Skapa och aktivera en virtuell miljö (valfritt men rekommenderat):

   ```bash

   python -m venv venv

   # Windows:

   .\venv\Scripts\activate

   # Linux/Mac:

   source venv/bin/activate

   ```
 
3. Installera dependencies:

   ```bash

   pip install -r requirements.txt

   ```
 
## Användning
 
Kör skriptet för att påbörja API-kedjan:
 
```bash

python Laboration1.py

```
 
## Funktionalitet

Verktyget hanterar följande steg:

1. Hämtar en session-token från `/api/token`.

2. Verifierar token och hämtar en hemlighet (secret) från `/api/verify`.

3. Skickar tillbaka token och secret till `/api/flag` för att hämta flaggan.
 
Skriptet inkluderar robust felhantering för nätverksfel och timeout. 
 