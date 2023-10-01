# Projekt zur Vorhersage der Immobilienpreise in Wien

# ToDo:
docstrings und Kommentare in jedem Code
in mlflow füge einen tag mit der Datenversion hinzu

Streamlit-Report:
Barchart
Wien-Karte mit Bezirke - interaktive mit Karte pro Jahr
Modell-Output Plot (Recherche) - in mlflow generieren und an streamlit weiterleiten

## Wie installiere ich die Dienste?
```bash
cd airflow
docker compose up -d
```
Das Standard Passwort ist **airflow** und der Username ist **airflow**.

## Datensatz
### Abkürzungen im Dataset
| Code | Ganzer Name |
|--------------|-----------|
| KG.Code | Katastralgemeindenummer (Cadastre Municipality Number) |
| Katastralgemeinde | Katastralgemeindename (Cadastre Municipality Name) |
| EZ | Einlagezahl (Deposit Number) |
| PLZ | Postleitzahl (Postal Code) |
| ON | Orientierungsnummer (Orientation Number) |
| Gst. | Grundstücksnummer (Property Number) |
| Gst.Fl. | Grundstücksfläche (Land Area) |
| ErwArt | Erwerbsart (Acquisition Type: Purchase Agreement, Municipal Council Resolution, etc.) |
| Schutzzone | Schutzzone (Protected Zone) |
| Wohnzone | Wohnzone (Residential Zone) |
| ÖZ | Örtliches Raumordnungsprogramm (Local Spatial Planning Program) |
| Bausperre | Bausperre (Building Restriction) |
| parz. | parzelliert (parceled), unparzelliert (not parceled) |
| VeräußererCode | Veräußerercode (Seller Code) see below|
| Erwerbercode | Erwerbercode (Buyer Code) see below |
| Anteile | Anteile (Shares) |
| Zähler | Zähler (Numerator) |
| Nenner | Nenner (Denominator) |
| BJ | Baujahr (Year of Construction) |
| TZ | Tagebuchzahl (Journal Number) |
| €/m² Gfl. | Kaufpreis pro m² Grundfläche in EUR (Purchase Price per Square Meter of Land Area in EUR) |
| Baureifgest | Baureifgestaltung (Development-ready Land) |
| % Widmung | Widmungsanteil (Zoning Share) |
| Baurecht | Baurecht (Building Right) |
| Stammeinlage | Stammeinlage (Capital Stock) |
| sonst_wid | sonstige Widmung (Other Zoning) |
| sonst_wid_prz | Anteil der sonstigen Widmung in % (Share of Other Zoning in %) |

### Käufer/Verkäufer Info

| Code | Ganzer Name |
|------|-----------|
| 1, 2, 4, 5, 6, 7, 10, 11, 12, 14 | Gebietskörperschaften und juristische Personen mit öffentlichem Charakter (e.g., Municipalities, States, Federal Government, Vienna Utilities, Austrian Federal Railways, etc.) |
| 3 | gemeinnützige Bauvereinigungen (e.g., Housing Cooperatives) |
| 8 | juristische Personen des Privatrechtes (e.g., Limited Liability Companies, Partnerships, Corporations, etc.) |
| 9 | Privatperson (Private Individual) |
| 13 | Bescheid Adressaten (e.g., Monetary Payment/Compensation... based on a decision in the course of creating building sites according to building regulations) |
