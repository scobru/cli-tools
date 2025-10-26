#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importiamo le librerie necessarie:
# 'os' per interagire con il sistema operativo (es. leggere file in una cartella)
# 'shutil' per operazioni avanzate sui file (es. spostarli)
import os
import shutil

def organizza_cartella():
    """Funzione principale che esegue la logica di organizzazione."""
    
    print("📂 Ciao! Questo script Python ti aiuterà a fare ordine.")
    target_dir = input("Inserisci il percorso completo della cartella da organizzare:\n> ")

    # --- PASSO 1: Controllare se la cartella esiste ---
    if not os.path.isdir(target_dir):
        print(f"❌ Errore: '{target_dir}' non è una cartella valida. Riprova.")
        return # Esce dalla funzione

    # --- PASSO 2: Ciclare su ogni elemento nella cartella ---
    try:
        for filename in os.listdir(target_dir):
            file_path = os.path.join(target_dir, filename)

            # Salta le sottocartelle per evitare di spostare una cartella dentro se stessa
            if os.path.isdir(file_path):
                continue

            # --- PASSO 3: Ottenere l'estensione del file ---
            # Troviamo la posizione dell'ultimo punto nel nome del file
            dot_index = filename.rfind('.')
            if dot_index == -1:
                continue # Salta i file senza estensione

            extension = filename[dot_index + 1:].lower()

            # --- PASSO 4: Creare la cartella di destinazione ---
            dest_folder_path = os.path.join(target_dir, extension)
            
            if not os.path.exists(dest_folder_path):
                os.makedirs(dest_folder_path)
                print(f"✅ Creata la cartella '{extension}'")

            # --- PASSO 5: Spostare il file ---
            dest_file_path = os.path.join(dest_folder_path, filename)
            
            # Se il file di destinazione esiste già, aggiungi un numero progressivo
            counter = 1
            original_name, original_ext = os.path.splitext(filename)
            while os.path.exists(dest_file_path):
                new_filename = f"{original_name}_{counter}{original_ext}"
                dest_file_path = os.path.join(dest_folder_path, new_filename)
                counter += 1
            
            shutil.move(file_path, dest_file_path)
            final_filename = os.path.basename(dest_file_path)
            print(f"Spostato '{filename}' in '{extension}/{final_filename}'")
            
        print("\n🎉 Organizzazione completata!")

    except Exception as e:
        print(f"Si è verificato un errore inaspettato: {e}")


# Questo blocco standard in Python assicura che il nostro codice
# venga eseguito solo quando lo script viene lanciato direttamente.
if __name__ == "__main__":
    organizza_cartella()
