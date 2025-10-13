import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os
import json
import hashlib
from datetime import datetime

class CryptoMessengerPro:
    def __init__(self, root):
        self.root = root
        self.root.title("CryptoMessenger Pro - Privacy Semplice e Sicura")
        self.root.geometry("900x750")
        self.root.configure(bg="#f8f9fa")
        
        # Dati applicazione
        self.private_key = None
        self.public_key = None
        self.contacts = {}  # Rubrica contatti
        self.config_file = "cryptomessenger_config.json"
        self.contacts_file = "cryptomessenger_contacts.json"
        
        self.load_config()
        self.load_contacts()
        self.setup_ui()
        
        # Mostra tutorial al primo avvio
        if not os.path.exists(self.config_file):
            self.show_welcome_tutorial()
    
    def setup_ui(self):
        # Stile moderno flat
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=12, font=('Segoe UI', 10), borderwidth=1, relief='flat')
        style.configure('Accent.TButton', background="#007bff", foreground="white")
        style.configure('TLabel', background="#f8f9fa", foreground="#2c3e50", font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), foreground="#2c3e50")
        style.configure('Subtitle.TLabel', font=('Segoe UI', 10), foreground="#6c757d")
        
        # Header elegante
        header = tk.Frame(self.root, bg="#ffffff", pady=25, relief='flat', bd=0)
        header.pack(fill=tk.X)
        
        title = ttk.Label(header, text="🔐 CryptoMessenger Pro", 
                         style='Title.TLabel', background="#ffffff")
        title.pack()
        
        subtitle = ttk.Label(header, text="Proteggi le tue conversazioni con crittografia end-to-end", 
                            style='Subtitle.TLabel', background="#ffffff")
        subtitle.pack()
        
        # Container principale
        main_container = tk.Frame(self.root, bg="#f8f9fa")
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        # Sezione Status e Azioni Rapide
        top_section = tk.Frame(main_container, bg="#f8f9fa")
        top_section.pack(fill=tk.X, pady=(0, 20))
        
        # Status
        status_frame = tk.LabelFrame(top_section, text=" 📊 Il Tuo Account ", 
                                     bg="#ffffff", fg="#2c3e50", font=('Segoe UI', 11, 'bold'),
                                     padx=20, pady=15, relief='flat', bd=1)
        status_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        self.status_label = ttk.Label(status_frame, text="⚠️ Account non configurato", 
                                      background="#ffffff", foreground="#dc3545",
                                      font=('Segoe UI', 11, 'bold'))
        self.status_label.pack(anchor=tk.W)
        
        self.fingerprint_label = ttk.Label(status_frame, text="", 
                                           background="#ffffff", foreground="#6c757d",
                                           font=('Consolas', 9))
        self.fingerprint_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Azioni rapide
        actions_frame = tk.LabelFrame(top_section, text=" ⚡ Azioni Rapide ", 
                                      bg="#ffffff", fg="#2c3e50", font=('Segoe UI', 11, 'bold'),
                                      padx=20, pady=15, relief='flat', bd=1)
        actions_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        
        ttk.Button(actions_frame, text="🔑 Configura Account", 
                  command=self.setup_wizard, style='Accent.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(actions_frame, text="👥 Gestisci Contatti", 
                  command=self.manage_contacts).pack(fill=tk.X, pady=2)
        ttk.Button(actions_frame, text="📤 Esporta Chiavi", 
                  command=self.export_keys_menu).pack(fill=tk.X, pady=2)
        ttk.Button(actions_frame, text="❓ Tutorial", 
                  command=self.show_welcome_tutorial).pack(fill=tk.X, pady=2)
        
        # Notebook principale
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # === TAB CRIPTA ===
        encrypt_frame = tk.Frame(notebook, bg="#f8f9fa")
        notebook.add(encrypt_frame, text="🔒 Invia Messaggio Sicuro")
        
        # Selezione destinatario
        dest_frame = tk.Frame(encrypt_frame, bg="#f8f9fa")
        dest_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(dest_frame, text="Destinatario:", bg="#f8f9fa", fg="#2c3e50", 
                font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT, padx=(0, 15))
        
        self.recipient_var = tk.StringVar()
        self.recipient_combo = ttk.Combobox(dest_frame, textvariable=self.recipient_var, 
                                           state="readonly", width=30)
        self.recipient_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.update_recipient_list()
        
        ttk.Button(dest_frame, text="➕ Nuovo Contatto", 
                  command=self.add_contact_quick).pack(side=tk.LEFT)
        
        # Area messaggio
        tk.Label(encrypt_frame, text="Il tuo messaggio:", 
                bg="#f8f9fa", fg="#2c3e50", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(20, 8))
        
        self.plain_text = scrolledtext.ScrolledText(encrypt_frame, height=10, 
                                                    font=('Segoe UI', 11), wrap=tk.WORD,
                                                    bg="#ffffff", fg="#2c3e50", insertbackground="#2c3e50",
                                                    relief='flat', bd=1)
        self.plain_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Opzioni crittografia
        options_frame = tk.Frame(encrypt_frame, bg="#f8f9fa")
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.sign_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="✍️ Firma digitalmente (raccomandato)", 
                      variable=self.sign_var, bg="#f8f9fa", fg="#2c3e50", 
                      selectcolor="#007bff", font=('Segoe UI', 10)).pack(side=tk.LEFT)
        
        tk.Label(options_frame, text="   Caratteri: ", bg="#f8f9fa", fg="#6c757d").pack(side=tk.LEFT)
        self.char_count = tk.Label(options_frame, text="0", bg="#f8f9fa", fg="#007bff", 
                                   font=('Segoe UI', 10, 'bold'))
        self.char_count.pack(side=tk.LEFT)
        
        self.plain_text.bind('<KeyRelease>', self.update_char_count)
        
        ttk.Button(encrypt_frame, text="🔒 CRIPTA E COPIA", 
                  command=self.encrypt_message_enhanced,
                  style='Accent.TButton').pack(pady=5)
        
        tk.Label(encrypt_frame, text="Messaggio criptato (pronto per essere inviato):", 
                bg="#f8f9fa", fg="#2c3e50", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(20, 8))
        
        self.encrypted_text = scrolledtext.ScrolledText(encrypt_frame, height=8, 
                                                       font=('Consolas', 10), wrap=tk.WORD,
                                                       bg="#ffffff", fg="#495057", relief='flat', bd=1)
        self.encrypted_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # === TAB DECRIPTA ===
        decrypt_frame = tk.Frame(notebook, bg="#f8f9fa")
        notebook.add(decrypt_frame, text="🔓 Leggi Messaggio Ricevuto")
        
        tk.Label(decrypt_frame, text="Incolla qui il messaggio criptato che hai ricevuto:", 
                bg="#f8f9fa", fg="#2c3e50", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(20, 8))
        
        input_frame = tk.Frame(decrypt_frame, bg="#f8f9fa")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.encrypted_input = scrolledtext.ScrolledText(input_frame, height=10, 
                                                        font=('Consolas', 10), wrap=tk.WORD,
                                                        bg="#ffffff", fg="#495057", 
                                                        insertbackground="#495057", relief='flat', bd=1)
        self.encrypted_input.pack(fill=tk.BOTH, expand=True)
        
        buttons_frame = tk.Frame(decrypt_frame, bg="#f8f9fa")
        buttons_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(buttons_frame, text="📋 Incolla dagli Appunti", 
                  command=self.paste_from_clipboard).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="🔓 DECRIPTA", 
                  command=self.decrypt_message_enhanced,
                  style='Accent.TButton').pack(side=tk.LEFT)
        
        tk.Label(decrypt_frame, text="Messaggio decriptato:", 
                bg="#f8f9fa", fg="#2c3e50", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(20, 8))
        
        self.decrypted_text = scrolledtext.ScrolledText(decrypt_frame, height=10, 
                                                       font=('Segoe UI', 11), wrap=tk.WORD,
                                                       bg="#d4edda", fg="#155724", relief='flat', bd=1)
        self.decrypted_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.decrypt_info = ttk.Label(decrypt_frame, text="", 
                                      background="#f8f9fa", foreground="#6c757d",
                                      font=('Segoe UI', 10))
        self.decrypt_info.pack(anchor=tk.W)
        
        self.update_status()
    
    def update_char_count(self, event=None):
        """Aggiorna contatore caratteri"""
        text = self.plain_text.get("1.0", tk.END).strip()
        self.char_count.config(text=str(len(text)))
    
    def show_welcome_tutorial(self):
        """Tutorial interattivo per nuovi utenti"""
        tutorial = tk.Toplevel(self.root)
        tutorial.title("Benvenuto in CryptoMessenger Pro!")
        tutorial.geometry("600x500")
        tutorial.configure(bg="#f8f9fa")
        tutorial.transient(self.root)
        tutorial.grab_set()
        
        tk.Label(tutorial, text="👋 Benvenuto!", bg="#f8f9fa", fg="#2c3e50",
                font=('Segoe UI', 22, 'bold')).pack(pady=25)
        
        text = """
CryptoMessenger Pro ti permette di inviare messaggi completamente 
privati attraverso qualsiasi piattaforma (WhatsApp, Telegram, email...).

🔐 COME FUNZIONA (in 3 semplici passi):

1️⃣ CONFIGURA IL TUO ACCOUNT
   • Crea la tua "identità digitale" (chiavi crittografiche)
   • È come avere una cassaforte personale con la tua chiave

2️⃣ AGGIUNGI I TUOI CONTATTI
   • Scambia le "chiavi pubbliche" con chi vuoi messaggiare
   • È come scambiarsi il numero della cassaforte (ma non la chiave!)
   
3️⃣ INVIA MESSAGGI SICURI
   • Scrivi il messaggio, cliccca "Cripta"
   • Copia e incolla su qualsiasi app di messaggistica
   • Solo il destinatario potrà leggerlo!

🛡️ PERCHÉ È SICURO:
   • Usa crittografia militare (RSA + AES)
   • Nemmeno noi possiamo leggere i tuoi messaggi
   • Le tue chiavi rimangono solo sul tuo computer

⚠️ IMPORTANTE:
   • NON perdere la tua chiave privata!
   • Fai sempre un backup in un posto sicuro
   • Non condividere MAI la chiave privata

Pronto a iniziare?
        """
        
        tk.Label(tutorial, text=text, bg="#f8f9fa", fg="#2c3e50",
                font=('Segoe UI', 11), justify=tk.LEFT).pack(padx=35, pady=25)
        
        btn_frame = tk.Frame(tutorial, bg="#f8f9fa")
        btn_frame.pack(pady=25)
        
        ttk.Button(btn_frame, text="🚀 Inizia Configurazione", 
                  command=lambda: [tutorial.destroy(), self.setup_wizard()]).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Chiudi", 
                  command=tutorial.destroy).pack(side=tk.LEFT)
    
    def setup_wizard(self):
        """Wizard guidato per configurazione iniziale"""
        wizard = tk.Toplevel(self.root)
        wizard.title("Configurazione Account")
        wizard.geometry("550x400")
        wizard.configure(bg="#f8f9fa")
        wizard.transient(self.root)
        wizard.grab_set()
        
        tk.Label(wizard, text="🔑 Configura il Tuo Account", bg="#f8f9fa", fg="#2c3e50",
                font=('Segoe UI', 18, 'bold')).pack(pady=25)
        
        info = """
Per usare CryptoMessenger, hai bisogno di:

1. Una CHIAVE PRIVATA (da tenere segreta)
2. Una CHIAVE PUBBLICA (da condividere con gli altri)

Scegli un'opzione:
        """
        
        tk.Label(wizard, text=info, bg="#f8f9fa", fg="#2c3e50",
                font=('Segoe UI', 11), justify=tk.LEFT).pack(padx=35, pady=15)
        
        btn_frame = tk.Frame(wizard, bg="#f8f9fa")
        btn_frame.pack(pady=25)
        
        def new_keys():
            wizard.destroy()
            self.generate_keys_with_password()
        
        def import_keys():
            wizard.destroy()
            self.import_private_key()
        
        ttk.Button(btn_frame, text="✨ Genera Nuove Chiavi (Raccomandato)", 
                  command=new_keys, style='Accent.TButton').pack(pady=10, fill=tk.X)
        ttk.Button(btn_frame, text="📥 Importa Chiavi Esistenti", 
                  command=import_keys).pack(pady=10, fill=tk.X)
        ttk.Button(btn_frame, text="Annulla", 
                  command=wizard.destroy).pack(pady=10)
    
    def generate_keys_with_password(self):
        """Genera chiavi con protezione password"""
        password = simpledialog.askstring("Password", 
                                         "Crea una password per proteggere la tua chiave privata:\n\n"
                                         "⚠️ IMPORTANTE: Non dimenticare questa password!\n"
                                         "Senza di essa non potrai leggere i tuoi messaggi.",
                                         show='*')
        if not password:
            return
        
        password_confirm = simpledialog.askstring("Conferma Password", 
                                                 "Conferma la password:", show='*')
        if password != password_confirm:
            messagebox.showerror("Errore", "Le password non corrispondono!")
            return
        
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
            self.update_status()
            
            messagebox.showinfo("✅ Successo!", 
                              "Account configurato correttamente!\n\n"
                              "Prossimi passi:\n"
                              "1. Esporta la tua chiave pubblica\n"
                              "2. Condividila con i tuoi contatti\n"
                              "3. Importa le chiavi pubbliche dei tuoi contatti")
            
            # Offri di esportare subito
            if messagebox.askyesno("Esporta Chiave Pubblica", 
                                   "Vuoi esportare ora la tua chiave pubblica?"):
                self.export_public_key()
        
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella generazione:\n{str(e)}")
    
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
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
                
        except Exception as e:
            raise Exception(f"Errore nel salvataggio: {str(e)}")
    
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
                
                # Chiave privata sarà caricata quando serve con password
            except:
                pass
    
    def load_private_key_with_password(self):
        """Carica chiave privata con password"""
        if self.private_key:
            return True
        
        if not os.path.exists(self.config_file):
            messagebox.showwarning("Attenzione", "Nessun account configurato!")
            return False
        
        password = simpledialog.askstring("Password", 
                                         "Inserisci la password del tuo account:", 
                                         show='*')
        if not password:
            return False
        
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
            messagebox.showerror("Errore", "Password errata o chiave corrotta!")
            return False
    
    def import_private_key(self):
        """Importa chiave privata esistente"""
        file_path = filedialog.askopenfilename(
            title="Seleziona la tua chiave privata",
            filetypes=[("File PEM", "*.pem"), ("Tutti i file", "*.*")]
        )
        
        if not file_path:
            return
        
        password = simpledialog.askstring("Password", 
                                         "Inserisci la password della chiave (lascia vuoto se non protetta):", 
                                         show='*')
        
        try:
            with open(file_path, 'rb') as f:
                key_data = f.read()
            
            pwd = password.encode() if password else None
            self.private_key = serialization.load_pem_private_key(
                key_data, password=pwd, backend=default_backend()
            )
            self.public_key = self.private_key.public_key()
            
            # Salva con nuova password
            new_password = simpledialog.askstring("Nuova Password", 
                                                 "Crea una password per proteggere la chiave:", 
                                                 show='*')
            if new_password:
                self.save_keys_with_password(new_password)
                self.update_status()
                messagebox.showinfo("Successo", "Chiave importata e salvata!")
            
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nell'importazione:\n{str(e)}")
    
    def export_public_key(self):
        """Esporta solo chiave pubblica"""
        if not self.public_key:
            messagebox.showwarning("Attenzione", "Nessuna chiave da esportare!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Salva la tua chiave pubblica",
            defaultextension=".pem",
            filetypes=[("File PEM", "*.pem")],
            initialfile="mia_chiave_pubblica.pem"
        )
        
        if not file_path:
            return
        
        try:
            public_pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            with open(file_path, 'wb') as f:
                f.write(public_pem)
            
            messagebox.showinfo("✅ Esportata!", 
                              f"Chiave pubblica salvata!\n\n"
                              f"📁 {file_path}\n\n"
                              f"Invia questo file ai tuoi contatti per permettergli "
                              f"di inviarti messaggi criptati.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nell'esportazione:\n{str(e)}")
    
    def export_keys_menu(self):
        """Menu per esportare chiavi"""
        if not self.public_key:
            messagebox.showwarning("Attenzione", "Nessun account configurato!\n\nConfigura prima il tuo account.")
            return
        
        export_win = tk.Toplevel(self.root)
        export_win.title("Esporta Chiavi")
        export_win.geometry("550x400")
        export_win.configure(bg="#f8f9fa")
        export_win.transient(self.root)
        export_win.grab_set()
        
        tk.Label(export_win, text="📤 Esporta le Tue Chiavi", bg="#f8f9fa", fg="#2c3e50",
                font=('Segoe UI', 18, 'bold')).pack(pady=25)
        
        info = """
Scegli quale chiave vuoi esportare:

🔓 CHIAVE PUBBLICA
   • Condividila liberamente con i tuoi contatti
   • Serve loro per inviarti messaggi criptati
   • È sicuro condividerla via email, chat, ecc.

🔐 CHIAVE PRIVATA
   • NON condividerla MAI con nessuno!
   • Esportala solo per fare un backup sicuro
   • Conservala in un posto molto sicuro
   • Chi la possiede può leggere i tuoi messaggi!
        """
        
        tk.Label(export_win, text=info, bg="#f8f9fa", fg="#2c3e50",
                font=('Segoe UI', 11), justify=tk.LEFT).pack(padx=35, pady=15)
        
        btn_frame = tk.Frame(export_win, bg="#f8f9fa")
        btn_frame.pack(pady=25)
        
        ttk.Button(btn_frame, text="🔓 Esporta Chiave Pubblica", 
                  command=lambda: [export_win.destroy(), self.export_public_key()]).pack(pady=10, fill=tk.X)
        ttk.Button(btn_frame, text="🔐 Esporta Chiave Privata (Backup)", 
                  command=lambda: [export_win.destroy(), self.export_private_key()]).pack(pady=10, fill=tk.X)
        ttk.Button(btn_frame, text="Annulla", 
                  command=export_win.destroy).pack(pady=10)
    
    def export_private_key(self):
        """Esporta chiave privata con avvertenze di sicurezza"""
        if not self.public_key:
            messagebox.showwarning("Attenzione", "Nessuna chiave da esportare!")
            return
        
        # Avvertenza di sicurezza
        warning = messagebox.askokcancel(
            "⚠️ ATTENZIONE - OPERAZIONE SENSIBILE",
            "Stai per esportare la tua CHIAVE PRIVATA!\n\n"
            "⚠️ PERICOLI:\n"
            "• Chi possiede questa chiave può leggere TUTTI i tuoi messaggi\n"
            "• NON inviarla MAI via email, chat o cloud non sicuri\n"
            "• Conservala solo su dispositivi sicuri e criptati\n\n"
            "✅ USI LEGITTIMI:\n"
            "• Backup sicuro su chiavetta USB criptata\n"
            "• Trasferimento su altro tuo dispositivo (con cautela)\n"
            "• Conservazione in cassaforte fisica\n\n"
            "Vuoi procedere con l'esportazione?"
        )
        
        if not warning:
            return
        
        # Richiede password per conferma
        if not self.load_private_key_with_password():
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Salva la tua chiave privata (TIENILA SEGRETA!)",
            defaultextension=".pem",
            filetypes=[("File PEM", "*.pem")],
            initialfile="mia_chiave_PRIVATA_backup.pem"
        )
        
        if not file_path:
            return
        
        # Chiede se proteggere con password
        protect = messagebox.askyesno(
            "Protezione Password",
            "Vuoi proteggere la chiave privata esportata con una password?\n\n"
            "RACCOMANDATO: Scegli 'Sì' per maggiore sicurezza"
        )
        
        try:
            if protect:
                export_password = simpledialog.askstring(
                    "Password Esportazione", 
                    "Crea una password per proteggere il file esportato:\n\n"
                    "(Può essere diversa dalla password del tuo account)",
                    show='*'
                )
                
                if not export_password:
                    messagebox.showinfo("Annullato", "Esportazione annullata.")
                    return
                
                export_password_confirm = simpledialog.askstring(
                    "Conferma Password", 
                    "Conferma la password:",
                    show='*'
                )
                
                if export_password != export_password_confirm:
                    messagebox.showerror("Errore", "Le password non corrispondono!")
                    return
                
                # Esporta con password
                private_pem = self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.BestAvailableEncryption(export_password.encode())
                )
            else:
                # Esporta senza password (NON RACCOMANDATO)
                messagebox.showwarning(
                    "Attenzione",
                    "⚠️ Stai esportando la chiave SENZA protezione password!\n\n"
                    "Chiunque acceda al file potrà leggere i tuoi messaggi!"
                )
                
                private_pem = self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            
            # Salva file
            with open(file_path, 'wb') as f:
                f.write(private_pem)
            
            messagebox.showinfo(
                "✅ Chiave Privata Esportata", 
                f"Chiave privata salvata con successo!\n\n"
                f"📁 {file_path}\n\n"
                f"🔐 Protetta con password: {'SÌ ✅' if protect else 'NO ⚠️'}\n\n"
                f"⚠️ IMPORTANTE:\n"
                f"• Conserva questo file in un luogo MOLTO sicuro\n"
                f"• NON condividerlo con nessuno\n"
                f"• NON caricarlo su cloud non sicuri\n"
                f"• Considera di salvarlo su USB criptata"
            )
        
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nell'esportazione:\n{str(e)}")
    
    def manage_contacts(self):
        """Gestione rubrica contatti"""
        contacts_win = tk.Toplevel(self.root)
        contacts_win.title("Rubrica Contatti")
        contacts_win.geometry("600x500")
        contacts_win.configure(bg="#f8f9fa")
        
        tk.Label(contacts_win, text="👥 I Tuoi Contatti", bg="#f8f9fa", fg="#2c3e50",
                font=('Segoe UI', 18, 'bold')).pack(pady=20)
        
        # Lista contatti
        list_frame = tk.Frame(contacts_win, bg="#f8f9fa")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        contacts_list = tk.Listbox(list_frame, font=('Segoe UI', 11), 
                                   bg="#ffffff", fg="#2c3e50",
                                   yscrollcommand=scrollbar.set, height=15, relief='flat', bd=1)
        contacts_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=contacts_list.yview)
        
        for name in self.contacts.keys():
            contacts_list.insert(tk.END, f"👤 {name}")
        
        # Pulsanti
        btn_frame = tk.Frame(contacts_win, bg="#f8f9fa")
        btn_frame.pack(pady=15)
        
        def add():
            self.add_contact()
            contacts_win.destroy()
            self.manage_contacts()
        
        def remove():
            selection = contacts_list.curselection()
            if selection:
                name = contacts_list.get(selection[0]).replace("👤 ", "")
                if messagebox.askyesno("Conferma", f"Eliminare {name}?"):
                    del self.contacts[name]
                    self.save_contacts()
                    contacts_list.delete(selection[0])
                    self.update_recipient_list()
        
        def view():
            selection = contacts_list.curselection()
            if selection:
                name = contacts_list.get(selection[0]).replace("👤 ", "")
                fingerprint = self.get_key_fingerprint(self.contacts[name])
                messagebox.showinfo(f"Dettagli: {name}", 
                                  f"Nome: {name}\n\n"
                                  f"Impronta digitale:\n{fingerprint}\n\n"
                                  f"Verifica questa impronta con il tuo contatto "
                                  f"tramite un canale sicuro (chiamata, di persona)")
        
        ttk.Button(btn_frame, text="➕ Aggiungi", command=add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Elimina", command=remove).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="👁️ Dettagli", command=view).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Chiudi", command=contacts_win.destroy).pack(side=tk.LEFT, padx=5)
    
    def add_contact_quick(self):
        """Aggiunta rapida contatto"""
        self.add_contact()
    
    def add_contact(self):
        """Aggiungi nuovo contatto"""
        name = simpledialog.askstring("Nuovo Contatto", 
                                     "Nome del contatto (es. Mario, Alice, ecc.):")
        if not name:
            return
        
        if name in self.contacts:
            messagebox.showwarning("Attenzione", "Contatto già esistente!")
            return
        
        file_path = filedialog.askopenfilename(
            title=f"Seleziona la chiave pubblica di {name}",
            filetypes=[("File PEM", "*.pem"), ("Tutti i file", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'rb') as f:
                key_data = f.read()
            
            public_key = serialization.load_pem_public_key(
                key_data, backend=default_backend()
            )
            
            # Salva come base64
            self.contacts[name] = base64.b64encode(key_data).decode()
            self.save_contacts()
            self.update_recipient_list()
            
            fingerprint = self.get_key_fingerprint(self.contacts[name])
            
            messagebox.showinfo("✅ Contatto Aggiunto!", 
                              f"{name} è stato aggiunto alla rubrica!\n\n"
                              f"Impronta digitale:\n{fingerprint}\n\n"
                              f"💡 Verifica questa impronta con {name} tramite "
                              f"chiamata o di persona per maggiore sicurezza.")
        
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nell'importazione:\n{str(e)}")
    
    def get_key_fingerprint(self, key_b64):
        """Genera fingerprint leggibile della chiave"""
        key_bytes = base64.b64decode(key_b64)
        hash_obj = hashlib.sha256(key_bytes)
        fingerprint = hash_obj.hexdigest().upper()
        # Formatta in blocchi di 4
        return ' '.join([fingerprint[i:i+4] for i in range(0, len(fingerprint), 4)])
    
    def save_contacts(self):
        """Salva rubrica"""
        with open(self.contacts_file, 'w') as f:
            json.dump(self.contacts, f)
    
    def load_contacts(self):
        """Carica rubrica"""
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, 'r') as f:
                    self.contacts = json.load(f)
            except:
                self.contacts = {}
    
    def update_recipient_list(self):
        """Aggiorna lista destinatari"""
        names = list(self.contacts.keys())
        self.recipient_combo['values'] = names
        if names and not self.recipient_var.get():
            self.recipient_combo.current(0)
    
    def update_status(self):
        """Aggiorna status account"""
        if self.public_key:
            self.status_label.config(text="✅ Account configurato e pronto", 
                                    foreground="#28a745")
            
            # Mostra fingerprint
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                fingerprint = self.get_key_fingerprint(config['public_key'])
                self.fingerprint_label.config(text=f"Impronta: {fingerprint[:35]}...")
            except:
                pass
        else:
            self.status_label.config(text="⚠️ Account non configurato", 
                                    foreground="#dc3545")
            self.fingerprint_label.config(text="")
    
    def encrypt_message_enhanced(self):
        """Crittografia ibrida AES+RSA con firma"""
        recipient = self.recipient_var.get()
        if not recipient:
            messagebox.showwarning("Attenzione", "Seleziona un destinatario!")
            return
        
        if recipient not in self.contacts:
            messagebox.showwarning("Attenzione", "Contatto non trovato!")
            return
        
        message = self.plain_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Attenzione", "Scrivi un messaggio!")
            return
        
        # Carica chiave privata se serve firmare
        if self.sign_var.get():
            if not self.load_private_key_with_password():
                return
        
        try:
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
            if self.sign_var.get() and self.private_key:
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
                'to': recipient
            }
            
            encrypted_text = base64.b64encode(json.dumps(packet).encode()).decode()
            
            self.encrypted_text.delete("1.0", tk.END)
            self.encrypted_text.insert("1.0", encrypted_text)
            
            # Copia automaticamente
            self.root.clipboard_clear()
            self.root.clipboard_append(encrypted_text)
            
            messagebox.showinfo("✅ Successo!", 
                              f"Messaggio criptato per {recipient}!\n\n"
                              f"✓ Il messaggio è stato copiato negli appunti\n"
                              f"✓ Lunghezza: {len(encrypted_text)} caratteri\n"
                              f"{'✓ Firmato digitalmente' if signature else ''}\n\n"
                              f"Ora puoi incollarlo su WhatsApp, Telegram, email, ecc.")
        
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nella crittografia:\n{str(e)}")
    
    def decrypt_message_enhanced(self):
        """Decrittografia ibrida con verifica firma"""
        if not self.load_private_key_with_password():
            return
        
        encrypted_text = self.encrypted_input.get("1.0", tk.END).strip()
        if not encrypted_text:
            messagebox.showwarning("Attenzione", "Incolla il messaggio ricevuto!")
            return
        
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
            if signature and sender in self.contacts:
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
            
            # Mostra messaggio
            self.decrypted_text.delete("1.0", tk.END)
            self.decrypted_text.insert("1.0", message)
            
            # Info aggiuntive
            info_text = f"📅 Inviato: {timestamp}\n"
            if signature:
                if signature_valid:
                    info_text += f"✅ Firma verificata da: {sender}"
                else:
                    info_text += f"⚠️ Firma non verificata (mittente sconosciuto o firma invalida)"
            
            self.decrypt_info.config(text=info_text)
            
            messagebox.showinfo("✅ Decriptato!", 
                              f"Messaggio decriptato con successo!\n\n{info_text}")
        
        except json.JSONDecodeError:
            messagebox.showerror("Errore", 
                               "Formato messaggio non valido.\n"
                               "Assicurati di aver copiato tutto il testo criptato.")
        except Exception as e:
            messagebox.showerror("Errore", 
                               f"Impossibile decrittare il messaggio.\n\n"
                               f"Possibili cause:\n"
                               f"• Il messaggio non era destinato a te\n"
                               f"• Il messaggio è corrotto\n"
                               f"• Formato non compatibile\n\n"
                               f"Dettagli: {str(e)}")
    
    def paste_from_clipboard(self):
        """Incolla dagli appunti"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.encrypted_input.delete("1.0", tk.END)
            self.encrypted_input.insert("1.0", clipboard_content)
        except:
            messagebox.showwarning("Attenzione", "Nessun testo negli appunti!")

def main():
    root = tk.Tk()
    app = CryptoMessengerPro(root)
    root.mainloop()

if __name__ == "__main__":
    main()