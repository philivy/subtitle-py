#!/bin/bash
# rendre executable ce script 
# $ chmod +x install.sh 
# $ ./install_script.sh

# Mettre à jour les dépôts et installer Python3 et pip
echo "Mise à jour des dépôts et installation de Python3 et pip..."
sudo apt update && sudo apt install -y python3 python3-pip python3-venv python3-tk
if [ $? -ne 0 ]; then
    echo "Échec de l'installation de Python3 et pip."
    exit 1
fi

# Vérifier la version de Python et pip
echo "Vérification de l'installation de Python et pip..."
python3 --version
pip3 --version
if [ $? -ne 0 ]; then
    echo "Échec de la vérification de la version de Python ou pip."
    exit 1
fi

# Créer un répertoire pour le projet (si ce n'est pas déjà fait)
echo "Création du répertoire du projet (si nécessaire)..."
mkdir -p ~/mon_projet
cd ~/mon_projet
if [ $? -ne 0 ]; then
    echo "Échec de la création du répertoire du projet."
    exit 1
fi

# Créer un environnement virtuel
echo "Création de l'environnement virtuel..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Échec de la création de l'environnement virtuel."
    exit 1
fi

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Échec de l'activation de l'environnement virtuel."
    exit 1
fi

# Installer les dépendances nécessaires
echo "Installation des bibliothèques nécessaires..."
pip install ffmpeg-python pysubs2 deepl cryptography
if [ $? -ne 0 ]; then
    echo "Échec de l'installation des bibliothèques nécessaires."
    exit 1
fi

# Vérifier que l'installation a réussi
echo "Vérification de l'installation des bibliothèques..."
pip list
if [ $? -ne 0 ]; then
    echo "Échec de la vérification des bibliothèques installées."
    exit 1
fi

# Installer FFmpeg (si ce n'est pas déjà installé)
echo "Installation de FFmpeg..."
sudo apt install -y ffmpeg
if [ $? -ne 0 ]; then
    echo "Échec de l'installation de FFmpeg."
    exit 1
fi

# Vérifier l'installation de FFmpeg
echo "Vérification de l'installation de FFmpeg..."
ffmpeg -version
if [ $? -ne 0 ]; then
    echo "Échec de la vérification de l'installation de FFmpeg."
    exit 1
fi

# Affichage final
echo "L'installation est terminée. L'environnement est prêt à être utilisé."

# Désactiver l'environnement virtuel
deactivate
if [ $? -ne 0 ]; then
    echo "Échec de la désactivation de l'environnement virtuel."
    exit 1
fi

