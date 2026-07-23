# 🔐 CryptoClipboard (Python CLI Edition)

Una versione Python cross-platform di `cryptoclip` che gira in background come icona di sistema (tray icon) e monitora/gestisce la clipboard con crittografia Fernet.

Questa implementazione è **100% compatibile** con la versione originale scritta in Rust.

---

## 🚀 Caratteristiche

*   **Global Hotkeys**: Funziona in background e risponde a scorciatoie globali da tastiera.
*   **Tray Icon**: Mostra una comoda icona nel system tray con un menu contestuale per eseguire tutte le operazioni.
*   **Clipboard Monitor**: Monitora la clipboard in tempo reale: se rileva testo cifrato compatibile con la chiave attiva, lo decifra automaticamente e lo stampa a terminale.
*   **Piena Compatibilità**: Cifra e decifra token compatibili con qualsiasi libreria Fernet standard (e con l'implementazione Rust).
*   **Fallback Robust**: Funziona in modalità solo terminale su sistemi headless (server, SSH) se la GUI non è disponibile.

---

## 📦 Requisiti e Installazione

Entra nella directory e installa le dipendenze:

```bash
cd cli-tools/cryptoclip
pip install -r requirements.txt
```

Le dipendenze principali sono:
*   `cryptography` (per cifratura Fernet)
*   `pyperclip` (per accesso alla clipboard)
*   `pynput` (per le scorciatoie globali)
*   `pystray` e `Pillow` (per l'icona e menu di sistema)

---

## ⌨️ Scorciatoie da Tastiera Attive

Quando il programma è in esecuzione:

| Scorciatoia | Azione |
|---|---|
| **`Ctrl + Shift + E`** | Cifra il testo attualmente in clipboard |
| **`Ctrl + Shift + D`** | Decifra il testo cifrato in clipboard |
| **`Ctrl + Shift + K`** | Genera una nuova chiave Fernet e la copia in clipboard |
| **`Ctrl + Shift + I`** | Importa una chiave Fernet dalla clipboard come chiave attiva |

---

## 🛠️ Utilizzo da Riga di Comando

### 1. Avviare in background / monitoraggio
```bash
python cryptoclip.py
```
Questo avvierà l'ascoltatore di tasti, il monitor della clipboard e la tray icon di sistema.

### 2. Specificare una chiave personalizzata all'avvio
Puoi passare la chiave tramite l'argomento `--key` o `-k`:
```bash
python cryptoclip.py -k "LaTuaChiaveFernetBase64..."
```
Oppure tramite la variabile d'ambiente `CRYPTO_CLIPBOARD_KEY`:
```bash
$env:CRYPTO_CLIPBOARD_KEY="LaTuaChiaveFernetBase64..."
python cryptoclip.py
```

### 3. Generare una nuova chiave al volo ed uscire
```bash
python cryptoclip.py --generate-key
# oppure
python cryptoclip.py genkey
```
Questo genererà una chiave valida a 32-byte in formato Base64, la stamperà a schermo e la copierà nella clipboard.
