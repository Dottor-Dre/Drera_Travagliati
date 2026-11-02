import csv
from datetime import datetime
 
FILE_MISURE = "Drera_Travagliati/dati/aria-brescia-misure-2026.csv"
FILE_SENSORI = "Drera_Travagliati/dati/aria-brescia-sensori.csv"
 
def carica(nomefile):
    righe_buone = []
    righe_scartate = 0
    sensori = {}
 
    with open(FILE_SENSORI, "r", encoding="utf-8-sig") as file:
        lettore = csv.DictReader(file)
 
        for riga in lettore:
            try:
                idsensore = riga["idsensore"].strip()
 
                sensori[idsensore] = {
                    "nometiposensore": riga["nometiposensore"].strip(),
                    "nomestazione": riga["nomestazione"].strip(),
                    "comune": riga["comune"].strip()
                }
 
            except (KeyError, AttributeError):
                continue
 
    with open(nomefile, "r", encoding="utf-8-sig") as file:
        lettore = csv.DictReader(file)
 
        for riga in lettore:
            try:
                idsensore = riga["idsensore"].strip()
                valore = float(riga["valore"].replace(",", "."))
                data = datetime.strptime(riga["data"].strip()[:10], "%Y-%m-%d")
 
                info = sensori[idsensore]
 
                nuova_riga = {
                    "idsensore": idsensore,
                    "data": data,
                    "valore": valore,
                    "stato": riga["stato"].strip(),
                    "nometiposensore": info["nometiposensore"],
                    "nomestazione": info["nomestazione"],
                    "comune": info["comune"]
                }
 
                righe_buone.append(nuova_riga)
 
            except (ValueError, KeyError, AttributeError):
                righe_scartate += 1
 
    return righe_buone, righe_scartate

def domanda1(dati):
    """Risponde alla domanda 1 della scheda."""
    return None


def domanda2(dati):
    """Risponde alla domanda 2."""
    return None


def domanda3(dati):
    """Risponde alla domanda 3. Restituisce la tabella
    che finirà in risultati.csv: una lista di righe."""
    return []


def domanda_nostra(dati):
    """La domanda inventata dal gruppo."""
    return None


def scrivi_risultati(nomefile, intestazione, tabella):
    """Scrive la tabella in un CSV con csv.writer."""
    pass


def main():
    dati, scartate = carica(FILE_MISURE)
    print(f"Righe buone: {len(dati)}, scartate: {scartate}")
    print("Domanda 1:", domanda1(dati))
    print("Domanda 2:", domanda2(dati))
    tabella = domanda3(dati)
    scrivi_risultati("risultati.csv", ["colonna1", "colonna2"], tabella)
    print("Domanda nostra:", domanda_nostra(dati))


main()