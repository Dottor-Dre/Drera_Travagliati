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
    totale = len(dati)
    valide = 0
    mancanti = 0
    sensori = {}
 
    for riga in dati:
        nome = riga["nomestazione"]
        inquinante = riga["nometiposensore"]
        codice = riga["idsensore"]
 
        if codice not in sensori:
            sensori[codice] = [nome, inquinante, 0]
 
        if riga["stato"] == "VA":
            valide += 1
        else:
            mancanti += 1
            sensori[codice][2] += 1
 
    massimo = 0
    stazione = ""
    inquinante = ""
 
    for codice in sensori:
        if sensori[codice][2] > massimo:
            massimo = sensori[codice][2]
            stazione = sensori[codice][0]
            inquinante = sensori[codice][1]
 
    return [totale, valide, mancanti, stazione, inquinante, massimo]


def domanda2(dati):
    valori = []
    giorno_massimo = ""
 
    for riga in dati:
        if ("PM10" in riga["nometiposensore"]
                and riga["nomestazione"] == "Brescia Villaggio Sereno"
                and riga["stato"] == "VA"):
 
            valore = riga["valore"]
            valori.append(valore)
 
            if valore == max(valori):
                giorno_massimo = riga["data"].strftime("%Y-%m-%d")
 
    if len(valori) == 0:
        return None
 
    minimo = min(valori)
    massimo = max(valori)
    media = sum(valori) / len(valori)
 
    return [minimo, massimo, round(media, 2), giorno_massimo]


def domanda3(dati):
    stazioni = {}
 
    for riga in dati:
        if "PM10" in riga["nometiposensore"] and riga["stato"] == "VA":
            nome = riga["nomestazione"]
            giorno = riga["data"].date()
 
            if nome not in stazioni:
                stazioni[nome] = {}
 
            if giorno not in stazioni[nome]:
                stazioni[nome][giorno] = [0, 0]
 
            stazioni[nome][giorno][0] += riga["valore"]
            stazioni[nome][giorno][1] += 1
 
    risultati = []
 
    for nome in stazioni:
        superamenti = 0
 
        for giorno in stazioni[nome]:
            media = stazioni[nome][giorno][0] / stazioni[nome][giorno][1]
 
            if media > 50:
                superamenti += 1
 
        risultati.append([
            nome,
            superamenti,
            "SI" if superamenti > 35 else "NO"
        ])
 
    for i in range(len(risultati)):
        for j in range(i + 1, len(risultati)):
            if risultati[j][1] > risultati[i][1]:
                risultati[i], risultati[j] = risultati[j], risultati[i]
 
    return risultati


def domanda_nostra(dati):
    """La domanda inventata dal gruppo."""
    return None


def scrivi_risultati(nomefile, intestazione, tabella):
    """Scrive la tabella in un CSV con csv.writer."""
    with open(nomefile, "w", encoding="utf-8", newline="") as file:
        scrittore = csv.writer(file)
        scrittore.writerow(intestazione)  
        scrittore.writerows(tabella)    
          


def main():
    dati, scartate = carica(FILE_MISURE)
    print(f"Righe buone: {len(dati)}, scartate: {scartate}")
    print("Domanda 1:", domanda1(dati))
    print("Domanda 2:", domanda2(dati))
    tabella = domanda3(dati)
    scrivi_risultati("risultati.csv", ["colonna1", "colonna2"], tabella)
    print("Domanda nostra:", domanda_nostra(dati))


main()