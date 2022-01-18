from sounddevice import Stream
from numpy import linalg
from pynput import keyboard
from tkinter import Tk, Label
from threading import Thread
from sys import argv


# emboiko/PttAlert - 10/3/2021
# Quick and dirty | Make sure Hux keeps his mic cued during raid ;)

class PttAlert:
    def __init__(self, threshold=0, window_width="350", window_height="225"):
        # Keyboard
        self.ptt_key = None

        # Microphone
        self.level = None
        self.cued = False
        self.threshold = int(threshold)

        # Tk Window
        self.window_width = window_width
        self.window_height = window_height
        self.win = Tk()
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.geometry(f"{self.window_width}x{self.window_height}")
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
            font=("Arial", 24)
        )
        self.message_label.grid()
        self.win.bind("<ButtonPress-1>", self.start_move)
        self.win.bind("<ButtonRelease-1>", self.stop_move)
        self.win.bind("<B1-Motion>", self.do_move)


    def start_move(self, event):
        self.x = event.x
        self.y = event.y


    def stop_move(self, event):
        self.x = None
        self.y = None


    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.win.winfo_x() + deltax
        y = self.win.winfo_y() + deltay
        self.win.geometry(f"+{x}+{y}")


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
        threshold=argv[1],
        window_width=argv[2],
        window_height=argv[3]
    )
    thread = Thread(target=alerter.init_input_stream, daemon=True)
    thread.start()
    alerter.win.mainloop()


if __name__ == "__main__":
    main()
