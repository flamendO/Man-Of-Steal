# REQUIREMENTS ----------------------------------------

pip install pyinstaller
pip install pywin32
pip install pycryptodome
pip install pycryptodomex
pip install requests
pip install urllib3

(Get-Content -Path "./src/dist/flags.txt" -Raw) -replace "(?m)^(.*\r?\n)(.*)$", "`${1}1" | Set-Content -Path "./src/dist/flags.txt"

Clear-Host
Write-Output "Installation of requirements done ! You can now open Gui interface !"
