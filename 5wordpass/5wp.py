import random
import string

def genera_passphrase_v2():
    print("--- GENERATORE DI PASSPHRASE MNEMONICHE V2 ---")
    print("Crea una storia assurda per una password a prova di bomba.\n")

    # 1. Raccolta degli input
    oggetto1 = input("1. Inserisci Oggetto/Cosa (es. tostapane): ").strip()
    colore1 = input("2. Inserisci Aggettivo/Colore (es. furioso): ").strip()
    azione = input("3. Inserisci Azione (es. lancia): ").strip()
    oggetto2 = input("4. Inserisci Altro Oggetto (es. fiamme): ").strip()
    aggettivo2 = input("5. Inserisci Aggettivo finale (es. digitali): ").strip()

    # Controllo campi vuoti
    if not all([oggetto1, colore1, azione, oggetto2, aggettivo2]):
        print("\nErrore: Hai lasciato dei campi vuoti! Riprova.")
        return

    parole = [oggetto1, colore1, azione, oggetto2, aggettivo2]

    # Generiamo elementi casuali per soddisfare i requisiti
    numero_casuale = random.randint(10, 99)  # Un numero a due cifre
    simbolo_casuale = random.choice("!@#$%&*") # Un simbolo sicuro

    # --- OPZIONE 1: PASSPHRASE ESTESA (Ora con numeri e simboli) ---
    # Uniamo le parole con trattini, ma aggiungiamo il numero e il simbolo alla fine
    # Es: Tostapane-Furioso-Lancia-Fiamme-Digitali-99!
    base_frase = "-".join([p.capitalize() for p in parole])
    passphrase_sicura = f"{base_frase}-{numero_casuale}{simbolo_casuale}"

    # --- OPZIONE 2: PASSWORD CONDENSATA (Aggiornata) ---
    # Iniziali + Numero totale lettere + Simbolo
    # Es: TFLFD36!
    iniziali = "".join([p[0].upper() for p in parole])
    lunghezza_totale = sum(len(p) for p in parole)
    # Assicuriamoci che la lunghezza sia visualizzata e aggiungiamo il simbolo usato sopra
    pass_condensata = f"{iniziali}{lunghezza_totale}{simbolo_casuale}"

    # 3. Output dei risultati
    print("\n" + "="*50)
    print("RISULTATI GENERATI (Policy-Friendly)")
    print("="*50)
    
    print(f"\n🔹 Frase originale: {oggetto1} {colore1} {azione} {oggetto2} {aggettivo2}")
    
    print("\n✅ OPZIONE 1 (Passphrase Completa):")
    print(f"   {passphrase_sicura}")
    print("   [Include: Maiuscole, Parole, Numeri, Simboli]")
    print("   (Perfetta per: Login principali, Master Password)")

    print("\n✅ OPZIONE 2 (Condensata):")
    print(f"   {pass_condensata}")
    print("   (Perfetta per: PIN lunghi, Wifi, Siti vecchi)")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    genera_passphrase_v2()