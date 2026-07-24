# 🛠️ CLI Tools Collection

Una raccolta di strumenti Python da riga di comando per aumentare la produttività quotidiana.

## 📋 Indice

- [clip](#-clip---clipboard-manager) - Gestore clipboard avanzato
- [cryptoclip](#-cryptoclip---clipboard-encryption) - Clipboard monitor e crittografia Fernet
- [cryptomessage](#-cryptomessage---encrypted-messaging) - Messaggistica crittografata end-to-end
- [dnote](#-dnote---zen-powered-developer-notebook) - Developer notebook con sync Zen relay
- [foldx](#-foldx---folder-organizer) - Organizzatore automatico di cartelle
- [opass](#-opass---organic-password-generator) - Generatore di password organiche

---

## 📋 clip - Clipboard Manager

Gestore avanzato della clipboard con cronologia persistente.

### Installazione
```bash
cd clip
pip install -r requirements.txt
```

### Utilizzo
```bash
# Salva contenuto corrente della clipboard
python clip.py save

# Salva testo direttamente
python clip.py put "Il mio testo importante"

# Mostra cronologia
python clip.py list

# Recupera un elemento (numero dalla lista)
python clip.py get 3

# Elimina un elemento
python clip.py delete 2

# Pulisci tutta la cronologia
python clip.py clear
```

### Caratteristiche
- ✅ Cronologia persistente salvata in `~/clipboard_history.json`
- ✅ Salvataggio rapido da clipboard
- ✅ Salvataggio diretto di testo
- ✅ Gestione multi-elemento

---

## 🔐 cryptoclip - Clipboard Encryption

Crittografia e decrittografia automatica o manuale del contenuto della clipboard tramite Fernet (compatibile con la versione Rust).

### Installazione
```bash
cd cryptoclip
pip install -r requirements.txt
```

### Utilizzo
```bash
# Avvio del monitor e del listener in background (con tray icon)
python cryptoclip.py

# Specifica una chiave personalizzata
python cryptoclip.py -k "LaTuaChiaveFernetBase64..."

# Genera una chiave al volo ed esci
python cryptoclip.py --generate-key
```

### Caratteristiche
- ✅ Monitor in background con auto-decriptazione
- ✅ Hotkeys globali: `Ctrl+Shift+E` (cifra), `Ctrl+Shift+D` (decifra), `Ctrl+Shift+K` (nuova chiave), `Ctrl+Shift+I` (carica chiave)
- ✅ System Tray Icon con menu rapido
- ✅ Fallback automatico in modalità headless/console se la GUI non è disponibile

---

## 🔐 cryptomessage - Encrypted Messaging

Applicazione GUI per inviare messaggi crittografati end-to-end tramite qualsiasi piattaforma.

### Installazione
```bash
cd cryptomessage
pip install -r requirements.txt
```

### Utilizzo
```bash
python cryptomessage.py
```

### Caratteristiche
- 🔒 Crittografia ibrida RSA-2048 + AES-256
- ✍️ Firma digitale dei messaggi
- 👥 Rubrica contatti con chiavi pubbliche
- 📤 Esporta/importa chiavi
- 🔐 Protezione password per chiavi private
- 🎨 Interfaccia grafica moderna e intuitiva

### Come funziona
1. **Configura account**: Genera o importa le tue chiavi crittografiche
2. **Aggiungi contatti**: Importa le chiavi pubbliche dei tuoi contatti
3. **Invia messaggi**: Scrivi, cripta e copia il messaggio
4. **Condividi**: Incolla su WhatsApp, Telegram, email, ecc.
5. **Ricevi**: Il destinatario decripta con la sua chiave privata

---

## 📝 editor - Terminal Text Editor

Editor di testo minimalista basato su curses per il terminale.

### Installazione
```bash
cd editor
pip install -r requirements.txt
```

### Utilizzo
```bash
# Crea/apri un file
python editor.py nomefile.txt

# Se non specifichi il nome, usa "nuovo_file.txt"
python editor.py
```

### Comandi
- **Frecce**: Naviga nel testo
- **Ctrl+S**: Salva file
- **Ctrl+Q**: Esci
- **Backspace**: Cancella carattere
- **Enter**: Nuova riga

---

## 📁 foldx - Folder Organizer

Organizza automaticamente i file in cartelle per estensione.

### Installazione
Nessuna dipendenza esterna richiesta (usa solo librerie standard).

### Utilizzo
```bash
cd foldx
python foldx.py
```

### Caratteristiche
- 📂 Organizza file per estensione automaticamente
- ✅ Crea cartelle al volo (jpg, pdf, txt, etc.)
- 🔒 Ignora le sottocartelle esistenti
- 💡 Interfaccia interattiva

### Esempio
```
Prima:
  /Downloads
    ├── foto1.jpg
    ├── documento.pdf
    ├── musica.mp3
    └── video.mp4

Dopo:
  /Downloads
    ├── jpg/
    │   └── foto1.jpg
    ├── pdf/
    │   └── documento.pdf
    ├── mp3/
    │   └── musica.mp3
    └── mp4/
        └── video.mp4
```

---

## 🌤️ meteocheck - Weather Checker

Controlla il meteo corrente e le previsioni da terminale usando l'API wttr.in.

### Installazione
```bash
cd meteocheck
pip install -r requirements.txt
```

### Utilizzo
```bash
# Meteo per una città
python meteocheck.py Roma
python meteocheck.py London
python meteocheck.py "New York"
```

### Output
- ☀️ Condizioni attuali
- 🌡️ Temperatura e temperatura percepita
- 💧 Umidità
- 📈 Previsioni domani (min/max)

---

## 🔑 opass - Organic Password Generator

Generatore di password memorabili basate su eventi significativi e trasformazioni combinate.

### Installazione
Nessuna dipendenza esterna richiesta (usa solo librerie standard).

### Utilizzo

#### Comandi Base
```bash
# Password base con trasformazione leet (default)
python opass.py holidays Christmas secret

# Lista tutti gli eventi disponibili
python opass.py --list

# Mostra esempi d'uso
python opass.py --examples

# Help completo
python opass.py -h
```

#### Esempi Avanzati
```bash
# Trasformazioni multiple (applicate in ordine)
python opass.py culture "Pi Day" myword -t reverse -t caps

# Anno personalizzato e struttura diversa
python opass.py history "Moon Landing (Apollo 11)" apollo -y 1969 -s d_s_k

# Concatenazione trasformazioni
python opass.py tech "iPhone Release" apple -t leet -t reverse

# Conversione alfanumerica
python opass.py personal "Custom Date 1" birthday -t alnum

# Case alternato
python opass.py seasons "Spring Equinox" flower -t alternate -s k_d_s
```

### Caratteristiche

#### 📅 Categorie Eventi (6 categorie, 42+ eventi)
- **holidays** [!] - Festività (9 eventi)
- **seasons** [#] - Stagioni (4 eventi)
- **culture** [$] - Eventi culturali (9 eventi)
- **history** [%] - Eventi storici (8 eventi)
- **personal** [&] - Date personalizzabili (5 slot)
- **tech** [@] - Milestone tecnologiche (7 eventi)

#### 🔄 Trasformazioni (6 tipi)
- **leet** - Converte vocali in numeri (a→@, e→3, i→1, o→0)
- **reverse** - Inverte la keyword
- **caps** - Tutto maiuscolo
- **alnum** - Lettere → numeri (a=1, b=2, ...)
- **alternate** - Alterna maiuscole/minuscole (aBaBaB)
- **vowelcaps** - Capitalizza solo le vocali

#### 🏗️ Strutture Password (6 varianti)
- **k_s_d** - Keyword-Symbol-Date (default)
- **d_s_k** - Date-Symbol-Keyword
- **s_k_d** - Symbol-Keyword-Date
- **k_d_s** - Keyword-Date-Symbol
- **d_k_s** - Date-Keyword-Symbol
- **s_d_k** - Symbol-Date-Keyword

### Output
- 🌿 Password in chiaro
- 🧠 Istruzioni per ricordarla
- 🔒 Hash SHA-256 (per storage sicuro)

---

## 🚀 Setup Rapido

### Installa tutte le dipendenze
```bash
# Dalla cartella cli-tools
pip install -r clip/requirements.txt
pip install -r cryptomessage/requirements.txt
pip install -r editor/requirements.txt
pip install -r meteocheck/requirements.txt

# foldx, opass e tasks non hanno dipendenze esterne
```

### Rendi gli script eseguibili (Linux/Mac)
```bash
chmod +x clip/clip.py
chmod +x cryptomessage/cryptomessage.py
chmod +x editor/editor.py
chmod +x foldx/foldx.py
chmod +x meteocheck/meteocheck.py
chmod +x opass/opass.py
chmod +x tasks/tasks.py
```

---

## 📦 Requisiti Sistema

- **Python**: 3.7+
- **OS**: Windows, Linux, macOS
- **Dipendenze**: Vedi `requirements.txt` in ogni sottocartella

---

## 🤝 Contribuire

Ogni tool è indipendente e può essere migliorato separatamente. 
Sentiti libero di:
- 🐛 Segnalare bug
- 💡 Proporre nuove funzionalità
- 🔧 Inviare pull request

---

## 📄 Licenza

Ogni tool può avere la propria licenza. Controlla i singoli progetti per dettagli.

---

## 🔗 Quick Reference

| Tool | Scopo | Dipendenze | GUI |
|------|-------|------------|-----|
| **clip** | Gestione clipboard | pyperclip | ❌ |
| **cryptomessage** | Messaggi criptati | cryptography | ✅ |
| **dnote** | Developer notebook | @akaoio/zen | ❌ |
| **foldx** | Organizza cartelle | - | ❌ |
| **opass** | Password | - | ❌ |

---

**Nota**: Alcuni tool richiedono dipendenze specifiche. Controlla sempre il file `requirements.txt` nella cartella del tool prima dell'uso.

