import json
from datetime import datetime
 
FILE_MISURE = "Drera_Travagliati/dati/aria-brescia-misure-2026.json"
FILE_SENSORI = "Drera_Travagliati/dati/aria-brescia-sensori.json"
 
def carica(nomefile):
    righe_buone = []
    righe_scartate = 0
    sensori = {}
 
    # Caricamento dei sensori da file JSON
    with open(FILE_SENSORI, "r", encoding="utf-8") as file:
        dati_sensori = json.load(file)
 
        for riga in dati_sensori:
            try:
                idsensore = str(riga["idsensore"]).strip()
 
                sensori[idsensore] = {
                    "nometiposensore": str(riga["nometiposensore"]).strip(),
                    "nomestazione": str(riga["nomestazione"]).strip(),
                    "comune": str(riga["comune"]).strip()
                }
 
            except (KeyError, AttributeError):
                continue
 
    # Caricamento delle misure da file JSON
    with open(nomefile, "r", encoding="utf-8") as file:
        dati_misure = json.load(file)
 
        for riga in dati_misure:
            try:
                idsensore = str(riga["idsensore"]).strip()
                
                # Gestione del valore (può essere stringa con virgola o numero)
                valore_raw = riga["valore"]
                if isinstance(valore_raw, str):
                    valore = float(valore_raw.replace(",", "."))
                else:
                    valore = float(valore_raw)

                data = datetime.strptime(str(riga["data"]).strip()[:10], "%Y-%m-%d")
 
                info = sensori[idsensore]
 
                nuova_riga = {
                    "idsensore": idsensore,
                    "data": data,
                    "valore": valore,
                    "stato": str(riga["stato"]).strip(),
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
    valori = {}

    for riga in dati:
        if "PM10" in riga["nometiposensore"] and riga["stato"] == "VA":
            comune = riga["comune"]

            if comune not in valori:
                valori[comune] = []

            valori[comune].append(riga["valore"])

    comune_migliore = None
    media_massima = 0

    for comune in valori:
        media = sum(valori[comune]) / len(valori[comune])

        if media > media_massima:
            media_massima = media
            comune_migliore = comune

    return comune_migliore, round(media_massima, 2)


def scrivi_risultati(nomefile, intestazione, tabella):
    """Converte la tabella in formato JSON strutturato e la salva su file."""
    dati_json = []
    for riga in tabella:
        elemento = {}
        for i, colonna in enumerate(intestazione):
            elemento[colonna] = riga[i]
        dati_json.append(elemento)

    with open(nomefile, "w", encoding="utf-8") as file:
        json.dump(dati_json, file, ensure_ascii=False, indent=4)
          

def main():
    dati, scartate = carica(FILE_MISURE)
    print(f"Righe buone: {len(dati)}, scartate: {scartate}")
    print("Domanda 1:", domanda1(dati))
    print("Domanda 2:", domanda2(dati))
    print("Domanda 3", domanda3(dati))
    tabella = domanda3(dati)
    scrivi_risultati("risultati.json", ["Stazione", "Giorni oltre 50", "Oltre 35 giorni"], tabella)
    print("Domanda nostra:", domanda_nostra(dati))
 
 
main()