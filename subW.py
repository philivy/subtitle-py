import os
import sys
import subprocess
import shutil
import pysubs2
import deepl
from cryptography.fernet import Fernet, InvalidToken

from tkinter import messagebox, filedialog, Tk, StringVar, OptionMenu, Button
import subprocess

# Définir trace_mode globalement
trace_mode = False  # Définition par défaut
trace_mode = True 

# Fonction de trace pour afficher les messages
def log_trace(message, log_file="trace.log"):
    print(message)
    if trace_mode:
        with open(log_file, "a") as log:
            log.write(message + "\n")

# Fonction pour générer et stocker une clé de chiffrement (si elle n'existe pas)
def generate_key():
    return Fernet.generate_key()

def store_encryption_key():
    key = generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Clé de chiffrement générée et stockée.")



def load_encryption_key():
       if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()
       else:
        messagebox.showerror("Erreur", "La clé de chiffrement n'a pas été trouvée. Génération en cours...")
        
        try:
            subprocess.run(["python", "cokW.py"], check=True)  # Lancement de cokW.py
            messagebox.showinfo("Succès", "La clé de chiffrement a été générée. Relancez l'application.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Erreur", "Échec de l'exécution de cokW.py.")
            return None
        
        return None


#################################################
# Chiffrer et déchiffrer la clé API
#################################################


"""def encrypt_api_key(api_key, encryption_key):
    f = Fernet(encryption_key)
    encrypted_key = f.encrypt(api_key.encode())
    print("Clé API chiffrée avec succès.")
    return encrypted_key"""

import subprocess
from cryptography.fernet import Fernet, InvalidToken

def decrypt_api_key(encrypted_key, encryption_key):
    try:
        if not encrypted_key:
            raise ValueError("La clé chiffrée est vide ou invalide.")

        f = Fernet(encryption_key)
        decrypted_key = f.decrypt(encrypted_key).decode()
        print("Clé API déchiffrée avec succès.")
        return decrypted_key

    except InvalidToken:
        print("Erreur : Impossible de déchiffrer la clé API. La clé de chiffrement est incorrecte ou le fichier est corrompu.")
    except ValueError as e:
        print(f"Erreur : {e}")
    except Exception as e:
        print(f"Erreur inattendue lors du déchiffrement : {e}")

    # Lancer cokW.py en cas d'erreur
    try:
        print("Tentative de régénération de la clé avec cokW.py...")
        subprocess.run(["python", "cokW.py"], check=True)
        print("Clé régénérée avec succès. Relancez l'application.")
    except subprocess.CalledProcessError:
        print("Erreur : Échec de l'exécution de cokW.py.")

    return None  # Retourne None en cas d'échec



#############################################
# Sélection du fichier vidéo
#############################################


def select_video_file():
    root = Tk()
    root.withdraw()  # Cacher la fenêtre principale
    video_file = filedialog.askopenfilename(
        title="Choisissez le fichier vidéo",
        filetypes=[("Fichiers vidéo", "*.mp4;*.mkv;*.avi"), ("Tous les fichiers", "*.*")]
    )
    
    log_trace(f"Fichier vidéo sélectionné : {video_file}")
    return video_file

# Fonction pour afficher en rouge
def print_red(text):
    print(f"\033[91m{text}\033[0m")  # Codes ANSI pour rouge

################################################################
# Fonction pour tester la connexion à l'API Deepl
#######################################################################
def get_api_key():    
    encryption_key = load_encryption_key()

    if encryption_key is None:
        return

    # Essayer de lire la clé API chiffrée si elle existe
    if os.path.exists("encrypted_api_key.enc"):
        print("Lecture de la clé API chiffrée...")
        with open("encrypted_api_key.enc", "rb") as enc_file:
            encrypted_key = enc_file.read()
        api_key = decrypt_api_key(encrypted_key, encryption_key)
                
        print("get_api_key:Clé API en clair :", api_key)

    # Déchiffrer la clé API pour l'utiliser avec DeepL
    api_key = decrypt_api_key(encrypted_key, encryption_key)

    return api_key

##################################################################
# Traduction des sous-titres avec l'API Deepl
###############################################################

def translate_subtitles(subtitle_file, target_lang):
    
    
    api_key =get_api_key()  

    translator = deepl.Translator(api_key)

    # Chargement des sous-titres
    subs = pysubs2.load(subtitle_file)
    
    # Traduction des sous-titres
    for line in subs:
        original_text = line.text
        
        # Vérification de la présence de "\n" ou "\N" et affichage en rouge
        if "\\n" in original_text or "\\N" in original_text:
            print_red(f"Texte original avec '\\n' ou '\\N' : {original_text}")  # Affichage en rouge
            # Remplacement de "\n" et "\N" par une chaîne vide
            original_text = original_text.replace("\\n", "").replace("\\N", "")
        
        # Traduction avec Deepl et extraction du texte traduit
        translated_text_result = translator.translate_text(original_text, target_lang=target_lang)
        translated_text = translated_text_result.text  # Extraction du texte traduit (chaîne)

        line.text = translated_text
        
        print(f"Texte traduit : {translated_text}")  # Affichage du texte traduit

    # Sauvegarder le fichier de sous-titres traduit
    translated_subtitle_path = subtitle_file.replace(".ass", f"_{target_lang}.ass")
    subs.save(translated_subtitle_path)
    log_trace(f"Sous-titres traduits et enregistrés : {translated_subtitle_path}")
    
    return translated_subtitle_path

#########################################################
# Lancer le traitement principal
#########################################################


def start_processing(video_file, target_lang, root):
    root.destroy()  # Fermer la fenêtre après validation

    trace_mode = False  # Par défaut, pas de mode trace
    log_file = "trace.log"

    if trace_mode:
        with open(log_file, "w") as log:
            log.write("Mode trace activé\n")

    def check_tools():
        tools = ["ffmpeg", "mkvextract", "mkvmerge"]
        for tool in tools:
            if not shutil.which(tool):
                log_trace(f"Erreur : {tool} n'est pas installé. Installation nécessaire.", log_file)
                sys.exit(1)

    def execute_command(command, error_message, log_file):
        log_trace(f"Exécution : {' '.join(command)}", log_file)
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            log_trace(error_message, log_file)
            sys.exit(1)

    def extract_subtitles():
        log_trace(f"Extraction des sous-titres de {video_file}...", log_file)
        subtitle_path = os.path.join(os.getcwd(), "subtitles.ass")
        if os.path.exists(subtitle_path):
            log_trace(f"Le fichier {subtitle_path} existe déjà, il sera écrasé.", log_file)
            os.remove(subtitle_path)
        
        execute_command(["ffmpeg", "-i", video_file, "-map", "0:s:0", subtitle_path],
                        "Erreur : Échec de l'extraction des sous-titres.", log_file)

        if os.path.exists(subtitle_path):
            file_size = os.path.getsize(subtitle_path)
            log_trace(f"Sous-titres extraits : {subtitle_path} ({file_size} octets)", log_file)

    def add_subtitles_to_mkv():
        output_video_file = os.path.splitext(video_file)[0] + f"_{target_lang.get().lower()}.mkv"
        subtitle_path = os.path.join(os.getcwd(), "subtitles.ass")

        # Traduction des sous-titres
        translated_subtitle_path = translate_subtitles(subtitle_path, target_lang.get().lower())

        execute_command([
    "mkvmerge", "-o", output_video_file, video_file,
    #"--track-name", "0:Original", subtitle_path,
    "--track-name", f"0:{target_lang.get().lower()}", translated_subtitle_path
        ], f"Erreur : Échec de l'ajout des sous-titres au fichier MKV.", log_file)

        
        log_trace(f"Fichier MKV créé : {output_video_file}", log_file)

        # Affichage du chemin du fichier vidéo avec les nouveaux sous-titres dans un popup
        messagebox.showinfo("Fichier créé", f"Le fichier vidéo avec sous-titres traduits a été créé :\n{output_video_file}")

    def check_file_existence():
        log_trace(f"Vérification de l'existence du fichier vidéo : {video_file}", log_file)
        if not os.path.isfile(video_file):
            log_trace("Erreur : Le fichier vidéo n'existe pas.", log_file)
            sys.exit(1)

    log_trace("Démarrage du traitement...", log_file)
    check_file_existence()
    check_tools()
    get_api_key()

    extract_subtitles()
    add_subtitles_to_mkv()
    log_trace("Traitement terminé avec succès.", log_file)


#######################################
# charge la liste des langues cibles
###################################### 

def get_deepl_target_languages(api_key):
    # Initialiser le traducteur Deepl avec la clé API
    translator = deepl.Translator(api_key)

    # Récupérer les langues cibles supportées
    target_languages = translator.get_target_languages()

    # Retourner la liste des codes de langues cibles (exemple: 'EN', 'FR')
    return [lang.code for lang in target_languages]

# Fonction principale
def main():
    global trace_mode

    # Création de la fenêtre Tkinter
    root = Tk()
    root.withdraw()  # Cacher la fenêtre principale

    # 1. Boîte de dialogue pour choisir le fichier vidéo
    video_file = filedialog.askopenfilename(
        title="Choisissez le fichier vidéo",
        filetypes=[("Fichiers vidéo", "*.mp4"), ("Fichiers vidéo", "*.mkv"), ("Fichiers vidéo", "*.avi"), ("Tous les fichiers", "*.*")]
    )
    
    # Affichage dans la console et écriture dans le log
    log_trace(f"Fichier vidéo sélectionné : {video_file}")
    
    if not video_file:
        messagebox.showerror("Erreur", "Aucun fichier vidéo sélectionné.")
        return
    
    # Récupérer la liste des langues Deepl
    api_key =get_api_key()  
    languages=get_deepl_target_languages(api_key)

 

    # 2. Création d'une nouvelle fenêtre pour la sélection de langue
    root = Tk()
    root.title("Sélectionnez une langue de traduction")
    root.geometry("300x200")

    # Liste déroulante pour choisir la langue
    target_lang = StringVar(root)
    
    target_lang.set("FR" if "FR" in languages else languages[0])  # Défaut à FR si dispo, sinon premier élément
    
    lang_menu = OptionMenu(root, target_lang, *languages)
    lang_menu.pack(pady=20)

    # Bouton "OK" pour lancer le programme
    ok_button = Button(root, text="OK", command=lambda: start_processing(video_file, target_lang, root))
    ok_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
