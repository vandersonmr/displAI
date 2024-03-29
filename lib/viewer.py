import tkinter as tk
from multiprocessing import Process, Value
import threading
from enum import Enum
from PIL import Image, ImageTk

class Viewer(threading.Thread):
    gif_files = [
        "gifs/listening.gif",
        "gifs/transcripting.gif",
        "gifs/thinking.gif",
        "gifs/speaking.gif",
        "gifs/startingsmall.gif"]

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.tk = tk.Tk()

        self.current_gif = 0

        self.tk.title("GIF Viewer")
        self.tk.geometry(
            "{0}x{1}+0+0".format(self.tk.winfo_screenwidth(), self.tk.winfo_screenheight()))
        self.tk.configure(background='black')
        self.tk.attributes('-fullscreen', True)

        self.tk.label2 = tk.Label(self.tk)
        self.tk.label = tk.Label(self.tk)
        self.tk.label2.pack()
        self.tk.label.pack()
        self.center_bottom_place(self.tk.label)

        self.load_gif()
        self.tk.mainloop()

    def show_image(self, image_path):
        # Load the image
        img = image_path#Image.open(image_path)

        # Get the screen dimensions
        screen_width = self.tk.winfo_screenwidth()
        screen_height = self.tk.winfo_screenheight()

        # Resize the image to fullscreen
        img = img.resize(
            (5 * screen_width // 5,
             5 * screen_height // 5))#,Image.ANTIALIAS)

        # Convert the image to a PhotoImage object
        photo_image = ImageTk.PhotoImage(img)

        # Update the label with the new image
        self.tk.label2.config(image=photo_image, borderwidth=0)
        self.tk.label2.image = photo_image
        self.tk.update()

    def center_bottom_place(self, widget, padding_y=0):
        widget.update()
        widget_width = widget.winfo_width()
        widget_height = widget.winfo_height()
        self.screen_width = self.tk.winfo_width()
        self.screen_height = self.tk.winfo_height()

        x = 0#(self.screen_width // 2) - (widget_width // 2)
        y = 0#self.screen_height - widget_height - padding_y

        widget.place(x=x, y=y) #place()

    def load_gif(self):
        self.gif = Image.open(self.gif_files[self.current_gif])#.resize((self.screen_width // 8,self.screen_width // 8))
        self.show()

    def show(self):
        try:
            frame = ImageTk.PhotoImage(self.gif)
            self.tk.label.config(image=frame, borderwidth=0)
            self.tk.label.image = frame
            self.gif.seek(self.gif.tell() + 1)
        except EOFError:
            self.gif.seek(0)
        except Exception:
            return

        self.tk.after(100, self.show)

    def change_state(self, state):
        if state == "sleep":
            self.show_gif(2)
        elif state == "awake":
            self.show_gif(0)
        elif state == "thinking":
            self.show_gif(4)
        elif state == "saying":
            self.show_gif(3)

    def show_gif(self, position):
        self.current_gif = position % len(self.gif_files)
        self.load_gif()
        self.center_bottom_place(self.tk.label)
