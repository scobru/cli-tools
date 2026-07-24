#!/usr/bin/env python3
import sys
import subprocess
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dnote_js = os.path.join(script_dir, "dnote.js")

    cmd = ["node", dnote_js] + sys.argv[1:]
    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except FileNotFoundError:
        print("Errore: Node.js non trovato nel sistema. Assicurati che Node.js sia installato e presente nel PATH.")
        sys.exit(1)
    except Exception as e:
        print(f"Errore durante l'esecuzione di dnote: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
