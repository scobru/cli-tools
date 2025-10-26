#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CryptoMessenger CLI - Versione da riga di comando
Crittografia end-to-end per messaggi sicuri via terminale
"""

import argparse
import sys
import os
import json
import base64
import hashlib
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import getpass

class CryptoMessengerCLI:
    def __init__(self):
        self.config_file = "cryptomessenger_config.json"
        self.contacts_file = "cryptomessenger_contacts.json"
        self.private_key = None
        self.public_key = None
        self.contacts = {}
        
        self.load_config()
        self.load_contacts()
    
    def load_config(self):
        """Carica configurazione"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                public_pem = base64.b64decode(config['public_key'])
                self.public_key = serialization.load_pem_public_key(
                    public_pem, backend=default_backend()
                )
            except:
                pass
    
    def load_contacts(self):
        """Carica rubrica"""
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, 'r') as f:
                    self.contacts = json.load(f)
            except:
                self.contacts = {}
    
    def save_config(self, config):
        """Salva configurazione"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
    
    def save_contacts(self):
        """Salva rubrica"""
        with open(self.contacts_file, 'w') as f:
            json.dump(self.contacts, f)
    
    def load_private_key_with_password(self, password=None):
        """Carica chiave privata con password"""
        if self.private_key:
            return True
        
        if not os.path.exists(self.config_file):
            print("❌ Nessun account configurato!")
            return False
        
        if not password:
            password = getpass.getpass("🔐 Password del tuo account: ")
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            private_pem = base64.b64decode(config['private_key'])
            self.private_key = serialization.load_pem_private_key(
                private_pem,
                password=password.encode(),
                backend=default_backend()
            )
            return True
            
        except Exception as e:
            print(f"❌ Password errata o chiave corrotta: {e}")
            return False
    
    def generate_keys(self):
        """Genera nuove chiavi"""
        print("🔑 Generazione nuove chiavi...")
        
        password = getpass.getpass("🔐 Crea una password per proteggere la tua chiave privata: ")
        password_confirm = getpass.getpass("🔐 Conferma la password: ")
        
        if password != password_confirm:
            print("❌ Le password non corrispondono!")
            return False
        
        try:
            # Genera chiavi
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            self.public_key = self.private_key.public_key()
            
            # Salva chiavi
            self.save_keys_with_password(password)
            
            print("✅ Account configurato correttamente!")
            print("📤 Esporta la tua chiave pubblica per condividerla con i contatti")
            return True
            
        except Exception as e:
            print(f"❌ Errore nella generazione: {e}")
            return False
    
    def save_keys_with_password(self, password):
        """Salva chiavi con cifratura"""
        try:
            # Cifra chiave privata con password
            private_pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
            )
            
            # Chiave pubblica non cifrata
            public_pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            config = {
                'private_key': base64.b64encode(private_pem).decode(),
                'public_key': base64.b64encode(public_pem).decode(),
                'created': datetime.now().isoformat()
            }
            
            self.save_config(config)
                
        except Exception as e:
            raise Exception(f"Errore nel salvataggio: {str(e)}")
    
    def export_public_key(self, filename=None):
        """Esporta chiave pubblica"""
        if not self.public_key:
            print("❌ Nessuna chiave da esportare!")
            return False
        
        if not filename:
            filename = "mia_chiave_pubblica.pem"
        
        try:
            public_pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            with open(filename, 'wb') as f:
                f.write(public_pem)
            
            print(f"✅ Chiave pubblica esportata: {filename}")
            print("📤 Invia questo file ai tuoi contatti per permettergli di inviarti messaggi criptati")
            return True
            
        except Exception as e:
            print(f"❌ Errore nell'esportazione: {e}")
            return False
    
    def export_keypair(self, filename=None, password=None):
        """Esporta keypair completo (chiave privata + pubblica)"""
        if not self.public_key:
            print("❌ Nessuna chiave da esportare!")
            return False
        
        if not self.load_private_key_with_password(password):
            return False
        
        if not filename:
            filename = "mia_chiave_PRIVATA_backup.pem"
        
        try:
            # Chiede se proteggere con password
            protect = True
            if not password:
                protect_input = input("🔐 Vuoi proteggere la chiave privata con una password? (s/n): ").lower()
                protect = protect_input in ['s', 'si', 'y', 'yes']
            
            if protect and not password:
                export_password = getpass.getpass("🔐 Password per proteggere il file esportato: ")
                export_password_confirm = getpass.getpass("🔐 Conferma la password: ")
                
                if export_password != export_password_confirm:
                    print("❌ Le password non corrispondono!")
                    return False
            else:
                export_password = password or ""
            
            # Esporta chiave privata
            if protect and export_password:
                private_pem = self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.BestAvailableEncryption(export_password.encode())
                )
            else:
                print("⚠️ ATTENZIONE: Stai esportando la chiave SENZA protezione password!")
                confirm = input("Sei sicuro? (s/n): ").lower()
                if confirm not in ['s', 'si', 'y', 'yes']:
                    print("❌ Esportazione annullata")
                    return False
                
                private_pem = self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            
            # Salva file
            with open(filename, 'wb') as f:
                f.write(private_pem)
            
            print(f"✅ Chiave privata esportata: {filename}")
            print(f"🔐 Protetta con password: {'SÌ ✅' if protect and export_password else 'NO ⚠️'}")
            print()
            print("⚠️ IMPORTANTE:")
            print("• Conserva questo file in un luogo MOLTO sicuro")
            print("• NON condividerlo con nessuno")
            print("• NON caricarlo su cloud non sicuri")
            print("• Considera di salvarlo su USB criptata")
            return True
            
        except Exception as e:
            print(f"❌ Errore nell'esportazione: {e}")
            return False
    
    def import_keypair(self, key_file, password=None):
        """Importa keypair esistente (chiave privata)"""
        if not os.path.exists(key_file):
            print(f"❌ File non trovato: {key_file}")
            return False
        
        try:
            # Leggi il file chiave
            with open(key_file, 'rb') as f:
                key_data = f.read()
            
            # Prova a caricare la chiave privata
            if not password:
                password = getpass.getpass("🔐 Password della chiave privata (lascia vuoto se non protetta): ")
            
            pwd = password.encode() if password else None
            
            try:
                self.private_key = serialization.load_pem_private_key(
                    key_data, password=pwd, backend=default_backend()
                )
            except Exception as e:
                if "incorrect password" in str(e).lower() or "bad decrypt" in str(e).lower():
                    print("❌ Password errata!")
                    return False
                else:
                    # Prova senza password
                    try:
                        self.private_key = serialization.load_pem_private_key(
                            key_data, password=None, backend=default_backend()
                        )
                        print("💡 Chiave caricata senza password")
                    except:
                        print(f"❌ Errore nel caricare la chiave: {e}")
                        return False
            
            # Estrai chiave pubblica
            self.public_key = self.private_key.public_key()
            
            # Chiedi nuova password per salvare
            new_password = getpass.getpass("🔐 Crea una nuova password per proteggere la chiave nel sistema: ")
            new_password_confirm = getpass.getpass("🔐 Conferma la nuova password: ")
            
            if new_password != new_password_confirm:
                print("❌ Le password non corrispondono!")
                return False
            
            # Salva con nuova password
            self.save_keys_with_password(new_password)
            
            print("✅ Keypair importato con successo!")
            print("🔐 Chiave salvata con nuova password")
            
            # Mostra fingerprint
            fingerprint = self.get_key_fingerprint_from_key(self.public_key)
            print(f"🔍 Impronta digitale: {fingerprint}")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore nell'importazione: {e}")
            return False
    
    def get_key_fingerprint_from_key(self, public_key):
        """Genera fingerprint da oggetto chiave pubblica"""
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        hash_obj = hashlib.sha256(public_pem)
        fingerprint = hash_obj.hexdigest().upper()
        return ' '.join([fingerprint[i:i+4] for i in range(0, len(fingerprint), 4)])
    
    def add_contact(self, name, key_file):
        """Aggiungi nuovo contatto"""
        if name in self.contacts:
            print(f"⚠️ Contatto '{name}' già esistente!")
            return False
        
        try:
            with open(key_file, 'rb') as f:
                key_data = f.read()
            
            public_key = serialization.load_pem_public_key(
                key_data, backend=default_backend()
            )
            
            # Salva come base64
            self.contacts[name] = base64.b64encode(key_data).decode()
            self.save_contacts()
            
            fingerprint = self.get_key_fingerprint(self.contacts[name])
            
            print(f"✅ Contatto '{name}' aggiunto!")
            print(f"🔍 Impronta digitale: {fingerprint}")
            print("💡 Verifica questa impronta con il contatto tramite chiamata o di persona")
            return True
        
        except Exception as e:
            print(f"❌ Errore nell'importazione: {e}")
            return False
    
    def get_key_fingerprint(self, key_b64):
        """Genera fingerprint leggibile della chiave"""
        key_bytes = base64.b64decode(key_b64)
        hash_obj = hashlib.sha256(key_bytes)
        fingerprint = hash_obj.hexdigest().upper()
        # Formatta in blocchi di 4
        return ' '.join([fingerprint[i:i+4] for i in range(0, len(fingerprint), 4)])
    
    def list_contacts(self):
        """Lista contatti"""
        if not self.contacts:
            print("📭 Nessun contatto nella rubrica")
            return
        
        print("👥 I tuoi contatti:")
        for name in self.contacts.keys():
            fingerprint = self.get_key_fingerprint(self.contacts[name])
            print(f"  👤 {name}")
            print(f"     🔍 {fingerprint[:35]}...")
            print()
    
    def encrypt_message(self, recipient, message, sign=True):
        """Cripta messaggio"""
        # Carica chiave privata se serve firmare
        if sign:
            if not self.load_private_key_with_password():
                return None
        
        try:
            # Gestione auto-messaggi (messaggio a se stessi)
            if recipient.lower() in ['me', 'io', 'self', 'me stesso']:
                if not self.public_key:
                    print("❌ Nessuna chiave pubblica disponibile!")
                    return None
                recipient_key = self.public_key
                print("💡 Messaggio auto-inviato (a te stesso)")
            else:
                if recipient not in self.contacts:
                    print(f"❌ Contatto '{recipient}' non trovato!")
                    print("💡 Suggerimento: Usa 'Me' per inviare messaggi a te stesso")
                    return None
                
                # Carica chiave pubblica destinatario
                recipient_key_pem = base64.b64decode(self.contacts[recipient])
                recipient_key = serialization.load_pem_public_key(
                    recipient_key_pem, backend=default_backend()
                )
            
            # Genera chiave AES casuale
            aes_key = os.urandom(32)  # 256 bit
            iv = os.urandom(16)
            
            # Cripta messaggio con AES
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            
            # Padding del messaggio
            message_bytes = message.encode('utf-8')
            padding_length = 16 - (len(message_bytes) % 16)
            padded_message = message_bytes + bytes([padding_length] * padding_length)
            
            encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
            
            # Cripta chiave AES con RSA
            encrypted_aes_key = recipient_key.encrypt(
                aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Firma (opzionale)
            signature = b""
            if sign and self.private_key:
                signature = self.private_key.sign(
                    encrypted_message,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
            
            # Crea pacchetto finale
            packet = {
                'version': '2.0',
                'aes_key': base64.b64encode(encrypted_aes_key).decode(),
                'iv': base64.b64encode(iv).decode(),
                'data': base64.b64encode(encrypted_message).decode(),
                'signature': base64.b64encode(signature).decode() if signature else "",
                'timestamp': datetime.now().isoformat(),
                'to': recipient if recipient.lower() not in ['me', 'io', 'self', 'me stesso'] else 'Me'
            }
            
            encrypted_text = base64.b64encode(json.dumps(packet).encode()).decode()
            
            print(f"✅ Messaggio criptato per {recipient}!")
            print(f"📏 Lunghezza: {len(encrypted_text)} caratteri")
            if signature:
                print("✍️ Firmato digitalmente")
            print()
            print("📋 Messaggio criptato:")
            print("-" * 50)
            print(encrypted_text)
            print("-" * 50)
            
            return encrypted_text
        
        except Exception as e:
            print(f"❌ Errore nella crittografia: {e}")
            return None
    
    def decrypt_message(self, encrypted_text, password=None):
        """Decripta messaggio"""
        if not self.load_private_key_with_password(password):
            return None
        
        try:
            # Decodifica pacchetto
            packet_json = base64.b64decode(encrypted_text).decode()
            packet = json.loads(packet_json)
            
            # Estrae componenti
            encrypted_aes_key = base64.b64decode(packet['aes_key'])
            iv = base64.b64decode(packet['iv'])
            encrypted_message = base64.b64decode(packet['data'])
            signature = base64.b64decode(packet['signature']) if packet.get('signature') else None
            timestamp = packet.get('timestamp', 'Sconosciuto')
            sender = packet.get('to', 'Sconosciuto')
            
            # Decripta chiave AES con RSA
            aes_key = self.private_key.decrypt(
                encrypted_aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Decripta messaggio con AES
            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
            
            # Rimuovi padding
            padding_length = padded_message[-1]
            message = padded_message[:-padding_length].decode('utf-8')
            
            # Verifica firma se presente
            signature_valid = False
            if signature:
                # Gestione firma per messaggi auto-inviati
                if sender.lower() in ['me', 'io', 'self', 'me stesso'] or sender == 'Me':
                    try:
                        # Per messaggi auto-inviati, usa la chiave pubblica corrente
                        if self.public_key:
                            self.public_key.verify(
                                signature,
                                encrypted_message,
                                padding.PSS(
                                    mgf=padding.MGF1(hashes.SHA256()),
                                    salt_length=padding.PSS.MAX_LENGTH
                                ),
                                hashes.SHA256()
                            )
                            signature_valid = True
                    except:
                        signature_valid = False
                elif sender in self.contacts:
                    try:
                        sender_key_pem = base64.b64decode(self.contacts[sender])
                        sender_key = serialization.load_pem_public_key(
                            sender_key_pem, backend=default_backend()
                        )
                        
                        sender_key.verify(
                            signature,
                            encrypted_message,
                            padding.PSS(
                                mgf=padding.MGF1(hashes.SHA256()),
                                salt_length=padding.PSS.MAX_LENGTH
                            ),
                            hashes.SHA256()
                        )
                        signature_valid = True
                    except:
                        signature_valid = False
            
            print("✅ Messaggio decriptato!")
            print(f"📅 Inviato: {timestamp}")
            if signature:
                if signature_valid:
                    print(f"✅ Firma verificata da: {sender}")
                else:
                    print("⚠️ Firma non verificata (mittente sconosciuto o firma invalida)")
            print()
            print("📝 Messaggio:")
            print("-" * 50)
            print(message)
            print("-" * 50)
            
            return message
        
        except json.JSONDecodeError:
            print("❌ Formato messaggio non valido")
            return None
        except Exception as e:
            print(f"❌ Impossibile decrittare il messaggio: {e}")
            return None
    
    def status(self):
        """Mostra status account"""
        if self.public_key:
            print("✅ Account configurato e pronto")
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                fingerprint = self.get_key_fingerprint(config['public_key'])
                print(f"🔍 Impronta: {fingerprint[:35]}...")
            except:
                pass
        else:
            print("⚠️ Account non configurato")
        
        print(f"👥 Contatti: {len(self.contacts)}")

def main():
    parser = argparse.ArgumentParser(
        description="CryptoMessenger CLI - Crittografia end-to-end per messaggi sicuri",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:

  # Configurazione iniziale
  python cryptomessage_cli.py setup
  python cryptomessage_cli.py export-key
  python cryptomessage_cli.py export-keypair

  # Importazione keypair esistente
  python cryptomessage_cli.py import-keypair backup_chiave_privata.pem

  # Gestione contatti
  python cryptomessage_cli.py add-contact Mario chiave_mario.pem
  python cryptomessage_cli.py list-contacts

  # Invio messaggio (ora supporta spazi!)
  python cryptomessage_cli.py encrypt Mario Ciao Mario come stai?

  # Ricezione messaggio
  python cryptomessage_cli.py decrypt "messaggio_criptato_base64..."

  # Status account
  python cryptomessage_cli.py status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandi disponibili')
    
    # Setup
    setup_parser = subparsers.add_parser('setup', help='Configura account iniziale')
    
    # Export key
    export_parser = subparsers.add_parser('export-key', help='Esporta chiave pubblica')
    export_parser.add_argument('-o', '--output', help='Nome file di output')
    
    # Export keypair
    export_pair_parser = subparsers.add_parser('export-keypair', help='Esporta keypair completo (chiave privata)')
    export_pair_parser.add_argument('-o', '--output', help='Nome file di output')
    
    # Import keypair
    import_pair_parser = subparsers.add_parser('import-keypair', help='Importa keypair esistente (chiave privata)')
    import_pair_parser.add_argument('key_file', help='File chiave privata da importare')
    
    # Add contact
    add_parser = subparsers.add_parser('add-contact', help='Aggiungi nuovo contatto')
    add_parser.add_argument('name', help='Nome del contatto')
    add_parser.add_argument('key_file', help='File chiave pubblica del contatto')
    
    # List contacts
    subparsers.add_parser('list-contacts', help='Lista contatti')
    
    # Encrypt
    encrypt_parser = subparsers.add_parser('encrypt', help='Cripta messaggio')
    encrypt_parser.add_argument('recipient', help='Nome destinatario')
    encrypt_parser.add_argument('message', nargs='+', help='Messaggio da criptare (può contenere spazi)')
    encrypt_parser.add_argument('--no-sign', action='store_true', help='Non firmare il messaggio')
    
    # Decrypt
    decrypt_parser = subparsers.add_parser('decrypt', help='Decripta messaggio')
    decrypt_parser.add_argument('encrypted_message', help='Messaggio criptato (base64)')
    
    # Status
    subparsers.add_parser('status', help='Mostra status account')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = CryptoMessengerCLI()
    
    if args.command == 'setup':
        cli.generate_keys()
    
    elif args.command == 'export-key':
        cli.export_public_key(args.output)
    
    elif args.command == 'export-keypair':
        cli.export_keypair(args.output)
    
    elif args.command == 'import-keypair':
        cli.import_keypair(args.key_file)
    
    elif args.command == 'add-contact':
        cli.add_contact(args.name, args.key_file)
    
    elif args.command == 'list-contacts':
        cli.list_contacts()
    
    elif args.command == 'encrypt':
        # Unisce tutte le parole del messaggio con spazi
        message = ' '.join(args.message)
        cli.encrypt_message(args.recipient, message, not args.no_sign)
    
    elif args.command == 'decrypt':
        cli.decrypt_message(args.encrypted_message)
    
    elif args.command == 'status':
        cli.status()

if __name__ == "__main__":
    main()
