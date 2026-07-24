#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import readline from "node:readline";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

// Import ZEN library relative to this script
import ZEN from "../../zen/index.js";

// ANSI Styling
const style = {
  reset: "\x1b[0m",
  bold: "\x1b[1m",
  dim: "\x1b[2m",
  italic: "\x1b[3m",
  cyan: "\x1b[36m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  red: "\x1b[31m",
  blue: "\x1b[34m",
  magenta: "\x1b[35m",
  bgCyan: "\x1b[46m\x1b[30m",
};

const DNOTE_DIR = process.env.DNOTE_HOME || path.join(os.homedir(), ".dnote");
const DATA_DIR = path.join(DNOTE_DIR, "data");
const CONFIG_FILE = path.join(DNOTE_DIR, "config.json");
const KEYPAIR_FILE = path.join(DNOTE_DIR, "keypair.json");

function ensureDirs() {
  if (!fs.existsSync(DNOTE_DIR)) fs.mkdirSync(DNOTE_DIR, { recursive: true });
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

function loadConfig() {
  ensureDirs();
  const defaultConfig = {
    relay: "https://delay.scobrudot.dev/zen",
    syncTimeoutMs: 2500,
  };
  if (!fs.existsSync(CONFIG_FILE)) {
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(defaultConfig, null, 2));
    return defaultConfig;
  }
  try {
    const raw = fs.readFileSync(CONFIG_FILE, "utf-8");
    return { ...defaultConfig, ...JSON.parse(raw) };
  } catch {
    return defaultConfig;
  }
}

async function getOrPairKeys() {
  ensureDirs();
  if (fs.existsSync(KEYPAIR_FILE)) {
    try {
      const raw = fs.readFileSync(KEYPAIR_FILE, "utf-8");
      return JSON.parse(raw);
    } catch (e) {
      // Regenerate if corrupt
    }
  }
  const pair = await ZEN.pair();
  fs.writeFileSync(KEYPAIR_FILE, JSON.stringify(pair, null, 2));
  return pair;
}

let zenInstance = null;
function initZen(config) {
  if (zenInstance) return zenInstance;
  zenInstance = new ZEN({
    file: DATA_DIR,
    peers: config.relay ? [config.relay] : [],
    localStorage: false,
  });
  return zenInstance;
}

// Generate short random ID for notes
function genId() {
  return "n_" + crypto.randomBytes(4).toString("hex");
}

// Helper to wait for async Zen read
function fetchAllNotes(zen, pubkey) {
  return new Promise((resolve) => {
    const notesMap = {};
    const timeout = setTimeout(() => resolve(notesMap), 800);

    zen.get("dnote_notes").get(pubkey).map().once((data, key) => {
      if (data && typeof data === "object" && data.id && data.book && data.content && !data.deleted) {
        notesMap[data.id] = {
          id: data.id,
          book: data.book,
          content: data.content,
          createdAt: data.createdAt || Date.now(),
          updatedAt: data.updatedAt || data.createdAt || Date.now(),
        };
      }
    });

    setTimeout(() => {
      clearTimeout(timeout);
      resolve(notesMap);
    }, 600);
  });
}

async function promptInput(questionText) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return new Promise((resolve) => {
    rl.question(questionText, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

async function promptMultilineInput(headerText) {
  console.log(`${style.cyan}${headerText}${style.reset}`);
  console.log(`${style.dim}(Scrivi il contenuto. Invia una riga vuota o premi Ctrl+D per salvare)${style.reset}`);

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const lines = [];
  return new Promise((resolve) => {
    rl.on("line", (line) => {
      if (line === "" && lines.length > 0) {
        rl.close();
        resolve(lines.join("\n"));
      } else {
        lines.push(line);
      }
    });
    rl.on("close", () => {
      resolve(lines.join("\n"));
    });
  });
}

// Subcommand handlers
async function cmdAdd(args, config, keypair) {
  const zen = initZen(config);
  let book = args[0];
  let content = "";

  if (!book) {
    console.error(`${style.red}Errore: Specifica il nome del taccuino/book.${style.reset}`);
    console.log(`Esempio: dnote add js "Usa Object.assign per clonare oggetti"`);
    process.exit(1);
  }

  // Check for -c flag
  const cIndex = args.indexOf("-c");
  if (cIndex !== -1 && args[cIndex + 1]) {
    content = args.slice(cIndex + 1).join(" ");
  } else if (args.length > 1) {
    content = args.slice(1).join(" ");
  }

  if (!content) {
    content = await promptMultilineInput(`Inserisci la nota per il taccuino '${book}':`);
  }

  if (!content.trim()) {
    console.log(`${style.yellow}Operazione annullata: Nota vuota.${style.reset}`);
    process.exit(0);
  }

  const id = genId();
  const now = Date.now();
  const noteData = {
    id,
    book,
    content,
    createdAt: now,
    updatedAt: now,
    deleted: false,
  };

  // Put into Zen local DB + sync
  zen.get("dnote_notes").get(keypair.pub).get(id).put(noteData);

  console.log(`\n${style.green}✔ Nota salvata con successo!${style.reset}`);
  console.log(`  ${style.dim}ID:${style.reset} ${style.bold}${id}${style.reset}`);
  console.log(`  ${style.dim}Book:${style.reset} ${style.blue}${book}${style.reset}`);
  console.log(`  ${style.dim}Sincronizzazione relay:${style.reset} ${style.cyan}${config.relay}${style.reset}\n`);

  setTimeout(() => process.exit(0), 400);
}

async function cmdView(args, config, keypair) {
  const zen = initZen(config);
  const notesMap = await fetchAllNotes(zen, keypair.pub);

  const bookArg = args[0];
  const noteIdArg = args[1];

  // Case 1: dnote view -> list all books with count
  if (!bookArg) {
    const books = {};
    Object.values(notesMap).forEach((n) => {
      books[n.book] = (books[n.book] || 0) + 1;
    });

    const bookNames = Object.keys(books).sort();
    if (bookNames.length === 0) {
      console.log(`\n${style.yellow}Nessun taccuino trovato.${style.reset}`);
      console.log(`Crea la tua prima nota con: ${style.bold}dnote add <book> "il tuo testo"${style.reset}\n`);
      process.exit(0);
    }

    console.log(`\n${style.bold}${style.bgCyan} 📚 I TUOI TACCUINI (BOOKS) ${style.reset}\n`);
    bookNames.forEach((b) => {
      const count = books[b];
      console.log(`  • ${style.bold}${style.blue}${b.padEnd(20)}${style.reset} ${style.dim}(${count} ${count === 1 ? "nota" : "note"})${style.reset}`);
    });
    console.log(`\n${style.dim}Per vedere le note di un taccuino: ${style.reset}${style.cyan}dnote view <book>${style.reset}\n`);
    process.exit(0);
  }

  // Case 2: dnote view <book> <note_id> -> view full note
  if (noteIdArg) {
    const note = notesMap[noteIdArg] || Object.values(notesMap).find(n => n.id === noteIdArg || n.id.endsWith(noteIdArg));
    if (!note || note.book.toLowerCase() !== bookArg.toLowerCase()) {
      console.error(`${style.red}Nota non trovata: ID '${noteIdArg}' nel taccuino '${bookArg}'${style.reset}`);
      process.exit(1);
    }

    const dateStr = new Date(note.createdAt).toLocaleString();
    console.log(`\n${style.bold}${style.cyan}----------------------------------------${style.reset}`);
    console.log(`${style.bold}Book:${style.reset} ${style.blue}${note.book}${style.reset} | ${style.bold}ID:${style.reset} ${style.dim}${note.id}${style.reset}`);
    console.log(`${style.bold}Data:${style.reset} ${style.dim}${dateStr}${style.reset}`);
    console.log(`${style.bold}${style.cyan}----------------------------------------${style.reset}\n`);
    console.log(note.content);
    console.log(`\n${style.bold}${style.cyan}----------------------------------------${style.reset}\n`);
    process.exit(0);
  }

  // Case 3: dnote view <book> -> list notes in book
  const bookNotes = Object.values(notesMap).filter(
    (n) => n.book.toLowerCase() === bookArg.toLowerCase()
  ).sort((a, b) => b.createdAt - a.createdAt);

  if (bookNotes.length === 0) {
    console.log(`\n${style.yellow}Nessuna nota trovata nel taccuino '${bookArg}'.${style.reset}\n`);
    process.exit(0);
  }

  console.log(`\n${style.bold}${style.cyan}📖 Taccuino: ${style.blue}${bookArg}${style.reset} ${style.dim}(${bookNotes.length} note)${style.reset}\n`);
  bookNotes.forEach((n, idx) => {
    const firstLine = n.content.split("\n")[0];
    const preview = firstLine.length > 70 ? firstLine.substring(0, 67) + "..." : firstLine;
    console.log(`  ${style.bold}${style.yellow}(${idx + 1})${style.reset} ${style.dim}[${n.id}]${style.reset} ${preview}`);
  });

  console.log(`\n${style.dim}Per leggere una nota completa: ${style.reset}${style.cyan}dnote view ${bookArg} <id>${style.reset}\n`);
  process.exit(0);
}

async function cmdEdit(args, config, keypair) {
  const zen = initZen(config);
  const notesMap = await fetchAllNotes(zen, keypair.pub);

  const bookArg = args[0];
  const noteIdArg = args[1];

  if (!bookArg || !noteIdArg) {
    console.error(`${style.red}Errore: Specifica sia il taccuino che l'ID della nota.${style.reset}`);
    console.log(`Uso: dnote edit <book> <note_id> [nuovo contenuto]`);
    process.exit(1);
  }

  const note = notesMap[noteIdArg] || Object.values(notesMap).find(n => n.id === noteIdArg || n.id.endsWith(noteIdArg));
  if (!note || note.book.toLowerCase() !== bookArg.toLowerCase()) {
    console.error(`${style.red}Nota non trovata: ID '${noteIdArg}' nel taccuino '${bookArg}'${style.reset}`);
    process.exit(1);
  }

  let newContent = args.slice(2).join(" ");
  if (!newContent) {
    console.log(`${style.dim}Contenuto attuale:${style.reset}\n${note.content}\n`);
    newContent = await promptMultilineInput(`Inserisci il nuovo contenuto per la nota [${note.id}]:`);
  }

  if (!newContent.trim()) {
    console.log(`${style.yellow}Operazione annullata: Contenuto vuoto.${style.reset}`);
    process.exit(0);
  }

  const updatedNote = {
    ...note,
    content: newContent,
    updatedAt: Date.now(),
  };

  zen.get("dnote_notes").get(keypair.pub).get(note.id).put(updatedNote);

  console.log(`\n${style.green}✔ Nota [${note.id}] aggiornata con successo!${style.reset}\n`);
  setTimeout(() => process.exit(0), 400);
}

async function cmdRemove(args, config, keypair) {
  const zen = initZen(config);
  const notesMap = await fetchAllNotes(zen, keypair.pub);

  const bookArg = args[0];
  const noteIdArg = args[1];

  if (!bookArg) {
    console.error(`${style.red}Errore: Specifica il nome del taccuino.${style.reset}`);
    console.log(`Uso: dnote rm <book> [note_id]`);
    process.exit(1);
  }

  // Remove specific note
  if (noteIdArg) {
    const note = notesMap[noteIdArg] || Object.values(notesMap).find(n => n.id === noteIdArg || n.id.endsWith(noteIdArg));
    if (!note || note.book.toLowerCase() !== bookArg.toLowerCase()) {
      console.error(`${style.red}Nota non trovata: ID '${noteIdArg}' nel taccuino '${bookArg}'${style.reset}`);
      process.exit(1);
    }

    zen.get("dnote_notes").get(keypair.pub).get(note.id).put({ ...note, deleted: true });
    console.log(`\n${style.green}✔ Nota [${note.id}] eliminata dal taccuino '${bookArg}'.${style.reset}\n`);
    setTimeout(() => process.exit(0), 400);
    return;
  }

  // Remove entire book
  const bookNotes = Object.values(notesMap).filter(
    (n) => n.book.toLowerCase() === bookArg.toLowerCase()
  );

  if (bookNotes.length === 0) {
    console.log(`${style.yellow}Nessuna nota trovata nel taccuino '${bookArg}'.${style.reset}`);
    process.exit(0);
  }

  const confirm = await promptInput(
    `Sei sicuro di voler eliminare TUTTE le ${bookNotes.length} note nel taccuino '${bookArg}'? (y/N): `
  );

  if (confirm.toLowerCase() === "y" || confirm.toLowerCase() === "yes") {
    bookNotes.forEach((n) => {
      zen.get("dnote_notes").get(keypair.pub).get(n.id).put({ ...n, deleted: true });
    });
    console.log(`\n${style.green}✔ Taccuino '${bookArg}' ed eliminato (${bookNotes.length} note rimosse).${style.reset}\n`);
  } else {
    console.log(`${style.yellow}Operazione annullata.${style.reset}`);
  }

  setTimeout(() => process.exit(0), 400);
}

async function cmdFind(args, config, keypair) {
  const query = args.join(" ").trim().toLowerCase();
  if (!query) {
    console.error(`${style.red}Errore: Specifica la parola chiave da cercare.${style.reset}`);
    console.log(`Uso: dnote find <query>`);
    process.exit(1);
  }

  const zen = initZen(config);
  const notesMap = await fetchAllNotes(zen, keypair.pub);

  const matches = Object.values(notesMap).filter(
    (n) => n.book.toLowerCase().includes(query) || n.content.toLowerCase().includes(query)
  );

  if (matches.length === 0) {
    console.log(`\n${style.yellow}Nessun risultato trovato per '${query}'.${style.reset}\n`);
    process.exit(0);
  }

  console.log(`\n${style.bold}${style.cyan}🔍 RISULTATI DELLA RICERCA PER '${query}' (${matches.length})${style.reset}\n`);

  matches.forEach((n) => {
    const lines = n.content.split("\n");
    const matchingLine = lines.find((l) => l.toLowerCase().includes(query)) || lines[0];
    console.log(`  • ${style.blue}[${n.book}]${style.reset} ${style.dim}[${n.id}]${style.reset} ${matchingLine}`);
  });

  console.log(`\n${style.dim}Per vedere una nota specifica: ${style.reset}${style.cyan}dnote view <book> <id>${style.reset}\n`);
  process.exit(0);
}

async function cmdSync(config) {
  console.log(`\n${style.cyan}🔄 Connessione e sincronizzazione con Zen Relay...${style.reset}`);
  console.log(`   ${style.dim}Relay URL:${style.reset} ${config.relay}`);

  const zen = initZen(config);
  const start = Date.now();

  await new Promise((resolve) => setTimeout(resolve, config.syncTimeoutMs || 2500));

  console.log(`${style.green}✔ Sincronizzazione completata con successo! (${Date.now() - start}ms)${style.reset}\n`);
  process.exit(0);
}

async function cmdStatus(config, keypair) {
  const zen = initZen(config);
  const notesMap = await fetchAllNotes(zen, keypair.pub);

  const totalNotes = Object.keys(notesMap).length;
  const books = new Set(Object.values(notesMap).map((n) => n.book));

  console.log(`\n${style.bold}${style.bgCyan} ⚡ DNOTE CONFIG & STATUS ${style.reset}\n`);
  console.log(`  ${style.bold}Sync Relay:${style.reset}   ${style.cyan}${config.relay}${style.reset}`);
  console.log(`  ${style.bold}Data Dir:${style.reset}     ${style.dim}${DATA_DIR}${style.reset}`);
  console.log(`  ${style.bold}Public Key:${style.reset}   ${style.yellow}${keypair.pub}${style.reset}`);
  console.log(`  ${style.bold}Taccuini:${style.reset}     ${style.blue}${books.size}${style.reset}`);
  console.log(`  ${style.bold}Total Note:${style.reset}   ${style.green}${totalNotes}${style.reset}\n`);

  process.exit(0);
}

async function cmdExport(args, config, keypair) {
  const zen = initZen(config);
  const notesMap = await fetchAllNotes(zen, keypair.pub);

  const jsonStr = JSON.stringify(Object.values(notesMap), null, 2);
  const outFile = args[0];

  if (outFile) {
    fs.writeFileSync(outFile, jsonStr, "utf-8");
    console.log(`\n${style.green}✔ Esportate ${Object.keys(notesMap).length} note in '${outFile}'${style.reset}\n`);
  } else {
    console.log(jsonStr);
  }
  process.exit(0);
}

async function cmdImport(args, config, keypair) {
  const inFile = args[0];
  if (!inFile || !fs.existsSync(inFile)) {
    console.error(`${style.red}Errore: Specifica un file JSON valido da importare.${style.reset}`);
    process.exit(1);
  }

  const zen = initZen(config);
  const raw = fs.readFileSync(inFile, "utf-8");
  const items = JSON.parse(raw);

  if (!Array.isArray(items)) {
    console.error(`${style.red}Errore: Il file di importazione deve contenere un array JSON di note.${style.reset}`);
    process.exit(1);
  }

  let count = 0;
  items.forEach((item) => {
    if (item.book && item.content) {
      const id = item.id || genId();
      const noteData = {
        id,
        book: item.book,
        content: item.content,
        createdAt: item.createdAt || Date.now(),
        updatedAt: item.updatedAt || Date.now(),
        deleted: false,
      };
      zen.get("dnote_notes").get(keypair.pub).get(id).put(noteData);
      count++;
    }
  });

  console.log(`\n${style.green}✔ Importate ${count} note con successo in Zen!${style.reset}\n`);
  setTimeout(() => process.exit(0), 400);
}

function showHelp() {
  console.log(`
${style.bold}${style.bgCyan} 📝 DNOTE CLI — Developer Notebook with Zen Relay Sync ${style.reset}

${style.bold}UTILIZZO:${style.reset}
  dnote <comando> [opzioni]

${style.bold}COMANDI:${style.reset}
  ${style.cyan}add <book> [testo]${style.reset}            Aggiunge una nota al taccuino <book>
  ${style.cyan}add <book> -c "testo"${style.reset}       Aggiunge una nota via flag -c
  ${style.cyan}view${style.reset}                          Lista tutti i taccuini (books)
  ${style.cyan}view <book>${style.reset}                   Lista tutte le note nel taccuino <book>
  ${style.cyan}view <book> <note_id>${style.reset}         Mostra il contenuto completo della nota
  ${style.cyan}edit <book> <note_id> [testo]${style.reset} Modifica una nota esistente
  ${style.cyan}rm <book> [note_id]${style.reset}           Elimina una nota o l'intero taccuino
  ${style.cyan}find <query>${style.reset}                  Cerca tra tutte le note (full-text)
  ${style.cyan}sync${style.reset}                          Sincronizza subito con Zen relay (${style.dim}delay.scobrudot.dev/zen${style.reset})
  ${style.cyan}status${style.reset}                        Mostra lo stato, chiavi e configurazione
  ${style.cyan}export [file.json]${style.reset}            Esporta le note in formato JSON
  ${style.cyan}import <file.json>${style.reset}            Importa note da file JSON

${style.bold}ESEMPI:${style.reset}
  dnote add js "Array.from({length: 5}) crea array di 5 elementi"
  dnote add git "git cherry-pick <commit-hash>"
  dnote view js
  dnote view js n_a1b2c3d4
  dnote find cherry-pick
  dnote sync
`);
}

// Entrypoint
async function main() {
  const config = loadConfig();
  const keypair = await getOrPairKeys();

  const rawArgs = process.argv.slice(2);
  if (rawArgs.length === 0 || rawArgs[0] === "-h" || rawArgs[0] === "--help" || rawArgs[0] === "help") {
    showHelp();
    process.exit(0);
  }

  const subcommand = rawArgs[0];
  const cmdArgs = rawArgs.slice(1);

  switch (subcommand) {
    case "add":
      await cmdAdd(cmdArgs, config, keypair);
      break;
    case "view":
    case "ls":
    case "list":
      await cmdView(cmdArgs, config, keypair);
      break;
    case "edit":
      await cmdEdit(cmdArgs, config, keypair);
      break;
    case "rm":
    case "remove":
    case "delete":
      await cmdRemove(cmdArgs, config, keypair);
      break;
    case "find":
    case "search":
      await cmdFind(cmdArgs, config, keypair);
      break;
    case "sync":
      await cmdSync(config);
      break;
    case "status":
    case "config":
      await cmdStatus(config, keypair);
      break;
    case "export":
      await cmdExport(cmdArgs, config, keypair);
      break;
    case "import":
      await cmdImport(cmdArgs, config, keypair);
      break;
    default:
      console.error(`${style.red}Comando sconosciuto: '${subcommand}'${style.reset}`);
      showHelp();
      process.exit(1);
  }
}

main().catch((err) => {
  console.error(`${style.red}Errore inatteso:${style.reset}`, err);
  process.exit(1);
});
