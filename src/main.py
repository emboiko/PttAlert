from sounddevice import Stream
from numpy import linalg
from pynput import keyboard
from tkinter import Tk, Label
from threading import Thread
from sys import argv


# emboiko/PttAlert - 10/3/2021
# Quick and dirty | Make sure Hux keeps his mic cued during raid ;)

class PttAlert:
    def __init__(self, threshold=0):
        # Keyboard
        self.ptt_key = None

        # Microphone
        self.level = None
        self.cued = False
        self.threshold = int(threshold)

        # Tk Window
        self.win = Tk()
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.geometry("450x300")
        self.win.update() 
        width_offset = int(
            (self.win.winfo_screenwidth() / 2) - (self.win.winfo_width() / 2)
        )
        height_offset = int(
            (self.win.winfo_screenheight() / 2) - (self.win.winfo_height() / 2)
        )
        self.win.geometry(f"+{width_offset}+{height_offset}")
        self.win.configure(bg="red")
        self.win.rowconfigure(0, weight=1)
        self.win.columnconfigure(0, weight=1)
        self.message_label = Label(
            self.win, 
            bg="red",
            font=("Arial", 30)
        )
        self.message_label.grid()


    def init_input_stream(self):
        with Stream(callback=self.processInput):
            listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            listener.start()
            listener.join()


    def processInput(self, indata, outdata, frames, time, status):
        volume_norm = linalg.norm(indata)*10
        self.level = int(volume_norm)

        if not self.ptt_key:
            self.message_label.configure(text="REGISTER PTT KEY")
            return
        else:
            self.message_label.configure(text=f"PUSH TO TALK\n NOT CUED\n\n{self.ptt_key}")

        if ((self.level > self.threshold) and (not self.cued)):
            self.win.configure(bg="red")
            self.win.attributes("-alpha", 1)
        else:
            self.win.attributes("-alpha", 0)
            self.win.configure(bg="black")


    def on_press(self, key):
        if key == keyboard.Key.ctrl_r:
            self.win.destroy()
            exit(0)

        if key == self.ptt_key:
            self.cued = True

        if not self.ptt_key:
            self.ptt_key = key


    def on_release(self, key):
        if key == self.ptt_key:
            self.cued = False


def main():
    alerter = PttAlert(
        threshold=argv[1]
    )
    thread = Thread(target=alerter.init_input_stream, daemon=True)
    thread.start()
    alerter.win.mainloop()


if __name__ == "__main__":
    main()
