# 📄 Scan to PDF Walkthrough (Canon TS5350i)

Uspio sam da podesim tvoj Canon TS5350i skener i napravim alatku za skeniranje više stranica direktno u PDF.

## 🚀 Kako pokrenuti skeniranje

1.  Otvori terminal u folderu `/home/kizabgd/Desktop/Istrazivanje/`.
2.  Pokreni skriptu komandom:
    ```bash
    ./multi_scan.py
    ```
3.  Prati uputstva na ekranu:
    -   Stavi papir na skener.
    -   Pritisni **ENTER**.
    -   Kada završi sa jednom stranom, pitaće te da li želiš još jednu (**y/N**).
    -   Na kraju će automatski spojiti sve u jedan PDF fajl.

## 📂 Lokacija fajlova

-   Skenirani dokumenti se čuvaju u folderu: `scans/` unutar tvog radnog direktorijuma.
-   Fajlovi su nazvani po datumu i vremenu (npr. `scan_20260224_174500.pdf`).

## 🛠️ Detalji implementacije

Napravljena skripta: [multi_scan.py](file:///home/kizabgd/Desktop/Istrazivanje/multi_scan.py)
Glavne funkcije:
-   **Automatska detekcija:** Sama pronalazi tvoj Canon uređaj preko USB-a.
-   **Multi-page:** Omogućava beskonačan broj strana dok god nastavljaš sa potvrdama.
-   **PDF Spajanje:** Koristi `img2pdf` biblioteku za visok kvalitet i optimalnu veličinu fajla.
-   **Čišćenje:** Automatski briše privremene slike nakon što napravi PDF.

Sada možeš lako arhivirati dokumente direktno sa svog Canon uređaja!
