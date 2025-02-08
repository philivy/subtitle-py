# subtitle-py
traduit les sous-titres avec deepl et ajoute la nouvelle piste traduite a la vidéo

1. abonnez vous gratuitement a DeepL Api

   https://www.deepl.com/pro?utm_source=github&utm_medium=github-java-readme#developer
   
   l'abonnement est gratuit mais une verification de carte bleue est obligatoire
   
   500 000 mots / mois gratuit 
     
2   lancer $ ./install.sh 

   active l'environnement python --->$ source /home/user/deepl-py/.venv/bin/activate
   le prompt du terminal doit changer --> (.venv) user@name-machine $ 

3   lancer $python cokW.py , saisir la clé DeepL ( apres l'abonnement gratuit ,sur le site , vous accederez a votre profil et à la clé Api

4   cokw va générer secret.key et  encrypted_api_key.enc , si la connection Api est ok. 

5   lancer $python subW.py

6   choissez votre vidéo et la langue cible      

