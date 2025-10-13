#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from pathlib import Path

# Definiamo il file dove verranno salvati i compiti
TASKS_FILE = Path.home() / '.tasks.json'

def load_tasks():
    """Carica i compiti dal file JSON. Se il file non esiste, lo crea."""
    if not TASKS_FILE.exists():
        return []
    with open(TASKS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return [] # Ritorna una lista vuota se il file è corrotto o vuoto

def save_tasks(tasks):
    """Salva la lista aggiornata dei compiti nel file JSON."""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(description):
    """Aggiunge un nuovo compito alla lista."""
    tasks = load_tasks()
    tasks.append({"description": description, "done": False})
    save_tasks(tasks)
    print(f"✅ Aggiunto compito: '{description}'")

def list_tasks():
    """Mostra tutti i compiti presenti nella lista."""
    tasks = load_tasks()
    if not tasks:
        print("🎉 Nessun compito in lista. Goditi il tempo libero!")
        return

    print("--- La Tua To-Do List ---")
    for i, task in enumerate(tasks):
        status = "✅" if task["done"] else "🔲"
        print(f"{i + 1}. {status} {task['description']}")

def complete_task(task_number):
    """Segna un compito come completato."""
    tasks = load_tasks()
    # L'utente vede i numeri da 1 in poi, ma la lista in Python parte da 0
    task_index = task_number - 1

    if 0 <= task_index < len(tasks):
        if tasks[task_index]["done"]:
            print(f"👍 Il compito '{tasks[task_index]['description']}' era già completato.")
        else:
            tasks[task_index]["done"] = True
            save_tasks(tasks)
            print(f"🎉 Completato: '{tasks[task_index]['description']}'")
    else:
        print(f"❌ Errore: Non esiste un compito con il numero {task_number}.")


def main():
    parser = argparse.ArgumentParser(description="Un semplice gestore di to-do list da terminale.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Comandi disponibili")

    # Comando 'add'
    parser_add = subparsers.add_parser("add", help="Aggiunge un nuovo compito.")
    parser_add.add_argument("description", type=str, help="La descrizione del compito.")
    parser_add.set_defaults(func=lambda args: add_task(args.description))

    # Comando 'list'
    parser_list = subparsers.add_parser("list", help="Mostra tutti i compiti.")
    parser_list.set_defaults(func=lambda args: list_tasks())

    # Comando 'done'
    parser_done = subparsers.add_parser("done", help="Segna un compito come completato.")
    parser_done.add_argument("task_number", type=int, help="Il numero del compito da completare.")
    parser_done.set_defaults(func=lambda args: complete_task(args.task_number))

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()