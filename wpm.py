import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the WPM-Typing Test! ")
    stdscr.addstr("\n Press any key to begin")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0, accuracy=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}  Accuracy: {accuracy}%")

    for i, char in enumerate(current):
        if i >= len(target):
            break
        correct_char = target[i]
        color = curses.color_pair(1) if char == correct_char else curses.color_pair(2)
        stdscr.addstr(0, i, char, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key:
            if ord(key) == 27:  # ESC
                return True
            elif key in ("KEY_BACKSPACE", '\b', "\x7f"):
                if current_text:
                    current_text.pop()
            elif len(current_text) < len(target_text):
                current_text.append(key)

        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        correct_chars = sum(1 for i, c in enumerate(current_text) if i < len(target_text) and c == target_text[i])
        accuracy = round((correct_chars / max(len(current_text), 1)) * 100)

        # Clear and redraw
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm, accuracy)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            return False



def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    start_screen(stdscr)
    while True:
        should_exit = wpm_test(stdscr)
        if should_exit:
            stdscr.clear()
            stdscr.addstr("Thanks for using WPM Tester! Goodbye 👋")
            stdscr.refresh()
            time.sleep(1.5)
            return

        stdscr.addstr(2, 0, "You completed the text! Press any key to continue or ESC to quit.")
        key = stdscr.getkey()
        if ord(key) == 27:
            stdscr.clear()
            stdscr.addstr("Thanks for using WPM Tester! Goodbye 👋")
            stdscr.refresh()
            time.sleep(1.5)
            return

wrapper(main)
