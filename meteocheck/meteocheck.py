#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import requests # Questa libreria serve per fare richieste HTTP (parlare con internet)
import sys

def get_meteo(citta):
    """
    Interroga l'API di wttr.in per ottenere i dati meteo in formato JSON
    e li stampa in modo leggibile.
    """
    # L'URL del servizio, con parametri per avere l'output in JSON ('j1')
    url = f"https://wttr.in/{citta}?format=j1"
    
    try:
        # Eseguiamo la richiesta al servizio web
        response = requests.get(url)
        # Controlliamo che la risposta sia andata a buon fine (codice 200)
        response.raise_for_status() 
        
        # Trasformiamo la risposta testuale in un dizionario Python (JSON)
        data = response.json()

        # --- Estraiamo i dati che ci interessano ---
        # Usiamo .get() per evitare errori se un campo non esiste
        condizioni_attuali = data.get('current_condition', [{}])[0]
        descrizione = condizioni_attuali.get('lang_it', [{}])[0].get('value', 'N/D')
        temp_c = condizioni_attuali.get('temp_C', 'N/D')
        temp_percepita_c = condizioni_attuali.get('FeelsLikeC', 'N/D')
        umidita = condizioni_attuali.get('humidity', 'N/D')
        
        meteo_domani = data.get('weather', [{}, {}])[1]
        temp_max_domani = meteo_domani.get('maxtempC', 'N/D')
        temp_min_domani = meteo_domani.get('mintempC', 'N/D')

        # --- Stampiamo il risultato in modo carino ---
        print("--- Meteo Attuale ---")
        print(f"📍 Città:         {citta.title()}")
        print(f"☀️  Condizioni:    {descrizione}")
        print(f"🌡️  Temperatura:   {temp_c}°C (Percepita: {temp_percepita_c}°C)")
        print(f"💧 Umidità:       {umidita}%")
        print("\n--- Previsioni Domani ---")
        print(f"📈 Temp. Max:     {temp_max_domani}°C")
        print(f"📉 Temp. Min:     {temp_min_domani}°C")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"❌ Errore: Città '{citta}' non trovata. Prova con il nome in inglese o un'altra città.")
        else:
            print(f"❌ Errore HTTP: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Errore di connessione: Controlla la tua connessione a internet. ({req_err})")
    except Exception as e:
        print(f"OPS! Si è verificato un errore inaspettato: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Mostra il meteo attuale per una data città usando wttr.in."
    )
    parser.add_argument(
        "citta", 
        type=str,
        help="Il nome della città per cui visualizzare il meteo."
    )
    args = parser.parse_args()
    
    get_meteo(args.citta)

if __name__ == "__main__":
    main()