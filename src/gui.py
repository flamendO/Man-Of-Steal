import customtkinter
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk


bg="black"
root = tk.Tk()
root.attributes("-fullscreen", False)
root.geometry("1000x600")
root.config(bg=bg)

def exit():
    root.destroy()

frame = tk.Frame(master=root)

#########LOGO######
img_logo = Image.open("./images/MOS_logo.png")
resized_logo = img_logo.resize((200,250), Image.Resampling.LANCZOS)
img_logo_resized = ImageTk.PhotoImage(resized_logo)

logo = tk.Label(root, image=img_logo_resized, bg=bg )
logo.pack()

#################



root.mainloop()