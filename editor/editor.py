import curses
import sys

def main(stdscr):
    # Inizializzazione di curses
    curses.curs_set(1)  # Mostra il cursore
    stdscr.clear()
    
    # Ottieni il nome del file dall'argomento della riga di comando
    filename = sys.argv[1] if len(sys.argv) > 1 else "nuovo_file.txt"
    
    try:
        with open(filename, "r") as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
    except FileNotFoundError:
        lines = [""]

    y, x = 0, 0
    top_line = 0

    while True:
        height, width = stdscr.getmaxyx()
        stdscr.clear()

        # Disegna la barra di stato in basso
        status_bar = f"File: {filename} | Ctrl+S per Salvare | Ctrl+Q per Uscire"
        stdscr.addstr(height - 1, 0, status_bar, curses.A_REVERSE)

        # Disegna le righe di testo
        for i, line in enumerate(lines[top_line:top_line + height - 1]):
            stdscr.addstr(i, 0, line)

        stdscr.move(y - top_line, x)
        stdscr.refresh()

        key = stdscr.getch()

        # Gestione dell'input
        if key == curses.KEY_UP:
            if y > 0:
                y -= 1
                if x > len(lines[y]):
                    x = len(lines[y])
        elif key == curses.KEY_DOWN:
            if y < len(lines) - 1:
                y += 1
                if x > len(lines[y]):
                    x = len(lines[y])
        elif key == curses.KEY_LEFT:
            if x > 0:
                x -= 1
        elif key == curses.KEY_RIGHT:
            if x < len(lines[y]):
                x += 1
        elif key == curses.KEY_BACKSPACE or key == 127:
            if x > 0:
                lines[y] = lines[y][:x - 1] + lines[y][x:]
                x -= 1
            elif y > 0:
                x = len(lines[y - 1])
                lines[y-1] += lines[y]
                del lines[y]
                y -= 1
        elif key == curses.KEY_ENTER or key == 10:
            lines.insert(y + 1, lines[y][x:])
            lines[y] = lines[y][:x]
            y += 1
            x = 0
        elif key == 19:  # Ctrl+S
            with open(filename, "w") as f:
                for line in lines:
                    f.write(line + '\n')
            stdscr.addstr(height - 2, 0, f"File '{filename}' salvato con successo!")
            stdscr.refresh()
            curses.napms(1500) # Attendi 1.5 secondi
        elif key == 17:  # Ctrl+Q
            break
        else:
            lines[y] = lines[y][:x] + chr(key) + lines[y][x:]
            x += 1

        # Gestione dello scorrimento
        if y < top_line:
            top_line = y
        if y >= top_line + height -1:
            top_line = y - height + 2


if __name__ == "__main__":
    curses.wrapper(main)