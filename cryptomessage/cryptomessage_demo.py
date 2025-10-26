#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Esempio di utilizzo di CryptoMessenger CLI
Dimostra come automatizzare l'invio di messaggi criptati
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Esegue comando e restituisce output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Errore: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Errore nell'esecuzione: {e}")
        return None

def check_setup():
    """Verifica se l'account è configurato"""
    status = run_command("python cryptomessage_cli.py status")
    if status and "Account configurato" in status:
        return True
    return False

def setup_account():
    """Configura account se non esiste"""
    print("🔑 Configurazione account...")
    result = run_command("python cryptomessage_cli.py setup")
    if result:
        print("✅ Account configurato!")
        return True
    return False

def export_public_key():
    """Esporta chiave pubblica"""
    print("📤 Esportazione chiave pubblica...")
    result = run_command("python cryptomessage_cli.py export-key -o mia_chiave_pubblica.pem")
    if result:
        print("✅ Chiave pubblica esportata!")
        return True
    return False

def add_contact(name, key_file):
    """Aggiunge contatto"""
    print(f"👤 Aggiunta contatto {name}...")
    result = run_command(f"python cryptomessage_cli.py add-contact {name} {key_file}")
    if result:
        print(f"✅ Contatto {name} aggiunto!")
        return True
    return False

def list_contacts():
    """Lista contatti"""
    print("👥 Lista contatti:")
    result = run_command("python cryptomessage_cli.py list-contacts")
    if result:
        print(result)
        return True
    return False

def send_message(recipient, message):
    """Invia messaggio criptato"""
    print(f"📤 Invio messaggio a {recipient}...")
    result = run_command(f'python cryptomessage_cli.py encrypt "{recipient}" "{message}"')
    if result:
        print("✅ Messaggio criptato!")
        return True
    return False

def decrypt_message(encrypted_message):
    """Decripta messaggio"""
    print("🔓 Decriptazione messaggio...")
    result = run_command(f'python cryptomessage_cli.py decrypt "{encrypted_message}"')
    if result:
        print("✅ Messaggio decriptato!")
        return True
    return False

def demo_workflow():
    """Dimostra il workflow completo"""
    print("🚀 Demo CryptoMessenger CLI")
    print("=" * 50)
    
    # 1. Verifica setup
    if not check_setup():
        print("⚠️ Account non configurato, procedo con la configurazione...")
        if not setup_account():
            print("❌ Impossibile configurare l'account")
            return False
    
    # 2. Esporta chiave pubblica
    if not os.path.exists("mia_chiave_pubblica.pem"):
        export_public_key()
    
    # 3. Lista contatti
    list_contacts()
    
    # 4. Esempio di invio messaggio (se ci sono contatti)
    contacts_result = run_command("python cryptomessage_cli.py list-contacts")
    if contacts_result and "Nessun contatto" not in contacts_result:
        print("\n📤 Esempio invio messaggio:")
        send_message("Mario", "Ciao Mario! Questo è un messaggio di test criptato.")
    else:
        print("\n💡 Per testare l'invio messaggi:")
        print("1. Aggiungi un contatto: python cryptomessage_cli.py add-contact Nome chiave.pem")
        print("2. Invia messaggio: python cryptomessage_cli.py encrypt Nome 'Il tuo messaggio'")
    
    print("\n✅ Demo completata!")
    return True

def interactive_mode():
    """Modalità interattiva"""
    print("🎯 Modalità Interattiva CryptoMessenger CLI")
    print("=" * 50)
    
    while True:
        print("\nComandi disponibili:")
        print("1. Status account")
        print("2. Lista contatti")
        print("3. Aggiungi contatto")
        print("4. Invia messaggio")
        print("5. Decripta messaggio")
        print("6. Esporta chiave pubblica")
        print("7. Demo completa")
        print("0. Esci")
        
        choice = input("\nScegli un'opzione (0-7): ").strip()
        
        if choice == "0":
            print("👋 Arrivederci!")
            break
        elif choice == "1":
            run_command("python cryptomessage_cli.py status")
        elif choice == "2":
            list_contacts()
        elif choice == "3":
            name = input("Nome contatto: ").strip()
            key_file = input("File chiave pubblica: ").strip()
            if name and key_file:
                add_contact(name, key_file)
        elif choice == "4":
            recipient = input("Destinatario: ").strip()
            message = input("Messaggio: ").strip()
            if recipient and message:
                send_message(recipient, message)
        elif choice == "5":
            encrypted = input("Messaggio criptato: ").strip()
            if encrypted:
                decrypt_message(encrypted)
        elif choice == "6":
            export_public_key()
        elif choice == "7":
            demo_workflow()
        else:
            print("❌ Opzione non valida!")

def main():
    """Funzione principale"""
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_workflow()
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
