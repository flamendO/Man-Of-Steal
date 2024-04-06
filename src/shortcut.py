import winshell
import os

# Chemin absolu complet vers l'exécutable
target = os.path.abspath("./src/dist/gui/gui.exe")

# Chemin absolu complet vers le dossier contenant l'exécutable
working_directory = os.path.dirname(target)

# Chemin absolu complet vers le fichier de raccourci avec extension .lnk
shortcut_path = os.path.abspath("./Man-Of-Steal.lnk")

# Créer le raccourci
shortcut = winshell.CreateShortcut(shortcut_path)
shortcut.TargetPath = target
shortcut.IconLocation = target  # Laissez-le vide pour utiliser l'icône de la cible
shortcut.Description = "Shortcut"

# Modifier le répertoire de travail du raccourci
shortcut.WorkingDirectory = working_directory

# Enregistrer le raccourci
shortcut.Save()
