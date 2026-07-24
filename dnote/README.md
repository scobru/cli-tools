# 📝 dnote — Zen-Powered Developer Notebook CLI

`dnote` è uno strumento da riga di comando per sviluppatori per prendere note veloci, organizzate in taccuini (*books*), con sincronizzazione offline-first e decentralizzata basata sul relay Zen **`https://delay.scobrudot.dev/zen`**.

Ispirato a [dnote](https://github.com/dnote/dnote), offre crittografia e identificazione crittografica tramite chiavi `ZEN.pair()`, persistenza locale immediata e sync automatico.

---

## ⚡ Caratteristiche

- 📚 **Organizzazione in Books**: Salva le tue note in categorie (`js`, `git`, `python`, `devops`, etc.).
- 🔄 **Zen Relay Sync**: Sincronizzazione automatica e offline-first con `https://delay.scobrudot.dev/zen`.
- 🔑 **Chiavi Crittografiche**: Generazione automatica della coppia di chiavi `ZEN.pair()` in `~/.dnote/keypair.json`.
- 🔍 **Ricerca Full-Text**: Trova all'istante qualsiasi nota cercando keyword in tutti i taccuini.
- 📤 **Export & Import**: Supporto nativo per l'esportazione/importazione di note in formato JSON.

---

## 📦 Installazione e Requisiti

- **Node.js**: ≥ 18
- Nessuna installazione complessa richiesta.

### Esecuzione Rapida:
```bash
cd cli-tools/dnote

# Tramite Node.js
node dnote.js help

# Tramite Python (wrapper)
python dnote.py status

# Tramite Batch Windows
dnote status
```

---

## 🚀 Utilizzo & Comandi

### 1. Aggiungere una Nota (`add`)
```bash
# Inserimento diretto
node dnote.js add js "Array.from({length: 5}) crea un array di 5 elementi"
node dnote.js add git "git commit --amend --no-edit"

# Tramite flag -c
node dnote.js add python -c "use list comprehension for fast inline filtering"

# Modalità multiriga interattiva (premi Invio su riga vuota per salvare)
node dnote.js add docker
```

### 2. Visualizzare i Taccuini e le Note (`view`)
```bash
# Elenca tutti i taccuini (books) con il conteggio note
node dnote.js view

# Elenca tutte le note all'interno del taccuino 'js'
node dnote.js view js

# Mostra il contenuto completo di una nota usando il suo ID (es: n_a1b2c3d4)
node dnote.js view js n_a1b2c3d4
```

### 3. Modificare una Nota (`edit`)
```bash
node dnote.js edit js n_a1b2c3d4 "Nuovo contenuto per la nota"
```

### 4. Eliminare Note o Taccuini (`rm`)
```bash
# Elimina una specifica nota
node dnote.js rm js n_a1b2c3d4

# Elimina l'intero taccuino (con conferma)
node dnote.js rm js
```

### 5. Cerca tra le Note (`find`)
```bash
node dnote.js find cherry-pick
```

### 6. Sincronizzazione Manuale con Zen Relay (`sync`)
```bash
node dnote.js sync
```

### 7. Configurazione e Stato (`status`)
```bash
node dnote.js status
```

### 8. Esportazione e Importazione (`export` / `import`)
```bash
# Esporta su file JSON
node dnote.js export mie_note.json

# Importa da file JSON
node dnote.js import mie_note.json
```
