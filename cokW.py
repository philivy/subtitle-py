import os
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import deepl


# 🔹 Générer et stocker la clé de chiffrement
def generate_key():
    return Fernet.generate_key()


def store_encryption_key():
    if os.path.exists("secret.key"):
        print("Clé de chiffrement déjà existante, chargement en cours...")
    else:
        key = generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        print("Clé de chiffrement générée et stockée.")


# 🔹 Charger la clé de chiffrement
def load_encryption_key():
    try:
        if os.path.exists("secret.key"):
            with open("secret.key", "rb") as key_file:
                key = key_file.read()
                print(f"Clé chargée : {key}")  # Ajoute ce print pour voir la clé
                if len(key) < 32:
                    raise ValueError("Clé corrompue ou invalide.")
                return key
        else:
            messagebox.showerror("Erreur", "La clé de chiffrement n'a pas été trouvée.")
            return None
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger la clé de chiffrement: {e}")
        return None


# 🔹 Chiffrer et déchiffrer la clé API
def encrypt_api_key(api_key, encryption_key):
    f = Fernet(encryption_key)
    encrypted_key = f.encrypt(api_key.encode())
    print("Clé API chiffrée avec succès.")
    return encrypted_key


def decrypt_api_key(encrypted_key, encryption_key):
    f = Fernet(encryption_key)
    decrypted_key = f.decrypt(encrypted_key).decode()
    print("Clé API déchiffrée avec succès.")
    return decrypted_key


# 🔹 Vérifier et régénérer les fichiers clés si nécessaire
def check_and_regenerate_keys():
    secret_key_file = "secret.key"
    encrypted_api_file = "encrypted_api_key.enc"

    secret_exists = os.path.exists(secret_key_file)
    encrypted_exists = os.path.exists(encrypted_api_file)

    if not secret_exists or not encrypted_exists:
        print("Un fichier manque, régénération en cours...")

        # Supprimer les fichiers existants
        if secret_exists:
            os.remove(secret_key_file)
            print("Fichier secret.key supprimé.")

        if encrypted_exists:
            os.remove(encrypted_api_file)
            print("Fichier encrypted_api_key.enc supprimé.")

        # Générer une nouvelle clé
        key = Fernet.generate_key()
        with open(secret_key_file, "wb") as key_file:
            key_file.write(key)

        print("Nouvelle clé de chiffrement générée et enregistrée.")


# 🔹 Tester la connexion DeepL
def test_connection():
    encryption_key = load_encryption_key()
    if encryption_key is None:
        return

    # Essayer de lire la clé API chiffrée si elle existe
    if os.path.exists("encrypted_api_key.enc"):
        print("Lecture de la clé API chiffrée...")
        with open("encrypted_api_key.enc", "rb") as enc_file:
            encrypted_key = enc_file.read()
        decrypted_key = decrypt_api_key(encrypted_key, encryption_key)
        entry_key.delete(0, tk.END)
        entry_key.insert(0, decrypted_key)
        print("Clé API en clair :", decrypted_key)

    # Récupérer la clé API entrée
    auth_key = entry_key.get()
    if not auth_key:
        messagebox.showwarning("Attention", "Veuillez entrer une clé API.")
        return

    # Stocker la clé API chiffrée
    encrypted_key = encrypt_api_key(auth_key, encryption_key)
    with open("encrypted_api_key.enc", "wb") as enc_file:
        enc_file.write(encrypted_key)
    print("Clé API mise à jour et enregistrée.")

    # Déchiffrer la clé API pour l'utiliser avec DeepL
    decrypted_key = decrypt_api_key(encrypted_key, encryption_key)

    try:
        print("Tentative de connexion à DeepL...")
        translator = deepl.Translator(decrypted_key)
        result = translator.translate_text("Test", target_lang="FR")
        messagebox.showinfo("Succès", f"Connexion réussie à DeepL. Réponse: {result.text}")
        print("Connexion réussie à DeepL.")

    except Exception as e:
        messagebox.showerror("Échec", f"Erreur de connexion à DeepL: {e}")
        print("Échec de la connexion à DeepL :", e)

        # Suppression de la clé API chiffrée en cas d'échec
        if os.path.exists("encrypted_api_key.enc"):
            os.remove("encrypted_api_key.enc")
            print("Clé API chiffrée supprimée après échec de connexion.")


# 🔹 Réinitialiser la clé API
def reset_api_key():
    if os.path.exists("encrypted_api_key.enc"):
        os.remove("encrypted_api_key.enc")
        print("Clé API chiffrée supprimée.")
        messagebox.showinfo("Réinitialisation", "La clé API a été réinitialisée.")
    entry_key.delete(0, tk.END)


# 🔹 Interface graphique Tkinter
root = tk.Tk()
root.title("Test de connexion DeepL")

tk.Label(root, text="Clé API DeepL:").pack(pady=5)
entry_key = tk.Entry(root, width=50)
entry_key.pack(pady=5)

tk.Button(root, text="Tester la connexion", command=test_connection).pack(pady=10)
tk.Button(root, text="Réinitialiser la clé API", command=reset_api_key, bg="red", fg="white").pack(pady=10)
"""
# Vérifier et générer la clé de chiffrement si nécessaire
if not os.path.exists("secret.key"):
    store_encryption_key()"""

# Vérifier et régénérer les fichiers clés si nécessaire
check_and_regenerate_keys()

# Vérifier si la clé API chiffrée existe et l'afficher
if os.path.exists("encrypted_api_key.enc"):
    encryption_key = load_encryption_key()
    if encryption_key is not None:
        with open("encrypted_api_key.enc", "rb") as enc_file:
            encrypted_key = enc_file.read()
        decrypted_key = decrypt_api_key(encrypted_key, encryption_key)
        entry_key.insert(0, decrypted_key)
        print("Clé API chargée depuis le fichier et affichée.")

print("Lancement de l'interface graphique...")
root.mainloop()
