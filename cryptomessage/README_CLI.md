# CryptoMessenger CLI

Versione da riga di comando di CryptoMessenger Pro per crittografia end-to-end veloce e semplice.

## 🚀 Installazione

```bash
# Installa le dipendenze
pip install cryptography

# Rendi eseguibile (Linux/Mac)
chmod +x cryptomessage_cli.py
```

## 📋 Comandi Disponibili

### 1. Configurazione Iniziale

```bash
# Configura il tuo account (genera chiavi)
python cryptomessage_cli.py setup

# Esporta la tua chiave pubblica
python cryptomessage_cli.py export-key
python cryptomessage_cli.py export-key -o mia_chiave.pem

# Esporta keypair completo (chiave privata) - PER BACKUP SICURO
python cryptomessage_cli.py export-keypair
python cryptomessage_cli.py export-keypair -o backup_chiave_privata.pem

# Importa keypair esistente (ripristina backup)
python cryptomessage_cli.py import-keypair backup_chiave_privata.pem
```

### 2. Gestione Contatti

```bash
# Aggiungi un contatto
python cryptomessage_cli.py add-contact Mario chiave_mario.pem

# Lista i tuoi contatti
python cryptomessage_cli.py list-contacts
```

### 3. Invio Messaggi

```bash
# Cripta un messaggio (ora supporta spazi senza virgolette!)
python cryptomessage_cli.py encrypt Mario Ciao Mario come stai?

# Cripta messaggio a te stesso (auto-messaggio)
python cryptomessage_cli.py encrypt Me Questo è un promemoria per me

# Cripta senza firma digitale
python cryptomessage_cli.py encrypt Mario Messaggio senza firma --no-sign
```

### 4. Ricezione Messaggi

```bash
# Decripta un messaggio ricevuto
python cryptomessage_cli.py decrypt "eyJ2ZXJzaW9uIjoiMi4wIiwiYWVzX2tleSI6Ii4uLiJ9"
```

### 5. Status Account

```bash
# Mostra status del tuo account
python cryptomessage_cli.py status
```

## 🔐 Esempi Pratici

### Scenario: Comunicazione tra Alice e Bob

**Alice configura il suo account:**
```bash
python cryptomessage_cli.py setup
python cryptomessage_cli.py export-key -o alice_public.pem
```

**Bob configura il suo account:**
```bash
python cryptomessage_cli.py setup
python cryptomessage_cli.py export-key -o bob_public.pem
```

**Alice aggiunge Bob ai contatti:**
```bash
python cryptomessage_cli.py add-contact Bob bob_public.pem
```

**Alice invia un messaggio a Bob:**
```bash
python cryptomessage_cli.py encrypt Bob Ciao Bob hai visto il nuovo progetto?
```

**Bob aggiunge Alice ai contatti:**
```bash
python cryptomessage_cli.py add-contact Alice alice_public.pem
```

**Bob decripta il messaggio di Alice:**
```bash
python cryptomessage_cli.py decrypt "messaggio_criptato_di_alice"
```

## 🔐 Esportazione Keypair Completo

Per fare backup sicuro della tua chiave privata:

```bash
# Esporta keypair con protezione password (RACCOMANDATO)
python cryptomessage_cli.py export-keypair

# Esporta con nome personalizzato
python cryptomessage_cli.py export-keypair -o backup_chiave_privata.pem
```

⚠️ **IMPORTANTE**: 
- La chiave privata permette di leggere TUTTI i tuoi messaggi
- Conservala in un luogo MOLTO sicuro
- NON condividerla MAI con nessuno
- Considera di salvarla su USB criptata

## 📥 Importazione Keypair

Per ripristinare un backup o trasferire le chiavi su un altro dispositivo:

```bash
# Importa keypair da backup
python cryptomessage_cli.py import-keypair backup_chiave_privata.pem

# Il sistema ti chiederà:
# 1. Password del file di backup (se protetto)
# 2. Nuova password per il sistema locale
```

**Casi d'uso:**
- 🔄 **Ripristino backup**: Recupera le chiavi da un backup
- 💻 **Trasferimento dispositivo**: Sposta le chiavi su un nuovo computer
- 🚨 **Recovery**: Ripristina l'accesso dopo perdita dati
- 🔧 **Migrazione**: Trasferisci account tra sistemi

**Sicurezza:**
- ✅ Chiave privata rimane sempre protetta
- ✅ Nuova password per il sistema locale
- ✅ Verifica fingerprint per conferma identità
- ✅ Compatibile con chiavi esportate da GUI e CLI

## 🛡️ Sicurezza

- **Crittografia ibrida**: RSA + AES per massima sicurezza
- **Firma digitale**: Verifica autenticità del mittente
- **Password**: Chiave privata protetta con password
- **Zero-knowledge**: Nemmeno noi possiamo leggere i tuoi messaggi

## 💡 Auto-Messaggi

Puoi inviare messaggi a te stesso usando:
- `Me` (inglese)
- `io` (italiano) 
- `self` (alternativo)
- `me stesso` (alternativo)

```bash
# Esempi di auto-messaggi
python cryptomessage_cli.py encrypt Me Promemoria: chiamare il cliente
python cryptomessage_cli.py encrypt io Appuntamento domani alle 15:00
python cryptomessage_cli.py encrypt self Password del server: xyz123
```

Questo è utile per:
- 📝 Promemoria personali
- 🔐 Conservare informazioni sensibili
- 📋 Note private criptate
- 💾 Backup di dati importanti

## 📱 Integrazione con App

Il messaggio criptato può essere copiato e incollato su:
- WhatsApp
- Telegram
- Email
- SMS
- Qualsiasi piattaforma di messaggistica

## 🔧 File di Configurazione

- `cryptomessenger_config.json`: Le tue chiavi (privata + pubblica)
- `cryptomessenger_contacts.json`: Rubrica contatti

## ⚠️ Note Importanti

1. **Backup**: Fai sempre backup della tua chiave privata
2. **Password**: Non dimenticare la password del tuo account
3. **Chiave privata**: NON condividerla MAI con nessuno
4. **Chiave pubblica**: Può essere condivisa liberamente

## 🆚 Differenze con la versione GUI

| Funzione | GUI | CLI |
|----------|-----|-----|
| Configurazione | Wizard guidato | Comando `setup` |
| Contatti | Interfaccia grafica | Comandi `add-contact`/`list-contacts` |
| Messaggi | Editor visuale | Input da terminale |
| Copia/Incolla | Automatico | Manuale |
| Velocità | Più lenta | Più veloce |
| Automazione | Limitata | Scriptabile |

## 🤖 Automazione

La versione CLI può essere facilmente integrata in script:

```bash
#!/bin/bash
# Script per inviare messaggio automatico

MESSAGE="Messaggio automatico"
RECIPIENT="Mario"
ENCRYPTED=$(python cryptomessage_cli.py encrypt "$RECIPIENT" "$MESSAGE")
echo "$ENCRYPTED" | xclip -selection clipboard
echo "Messaggio copiato negli appunti!"
```

## 🔍 Troubleshooting

**Errore "Account non configurato":**
```bash
python cryptomessage_cli.py setup
```

**Errore "Password errata":**
- Verifica di aver inserito la password corretta
- Se persiste, reimposta l'account con `setup`

**Errore "Contatto non trovato":**
```bash
python cryptomessage_cli.py list-contacts
python cryptomessage_cli.py add-contact Nome chiave.pem
```

**Errore "Formato messaggio non valido":**
- Assicurati di aver copiato tutto il messaggio criptato
- Il messaggio deve essere in formato base64
