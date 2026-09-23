Trier ses commentaires YouTube avec Laya — 100 % local, gratuit
L'Après IA · https://www.youtube.com/@LApresIA

CONTENU
  trier_commentaires.py      le script de la démo
  commentaires.csv           20 commentaires d'exemple (remplace-les par les tiens)
  INSTALLATION_windows.md    l'installation pas à pas

INSTALLATION (Windows, sans carte graphique)
  1. Installe Python 3.12 depuis python.org, en cochant « Add python.exe to PATH ».
  2. Ouvre ce dossier, clique dans la barre d'adresse, tape cmd puis Entrée.
  3. Colle ces quatre lignes, une par une :

     py -3.12 -m venv laya-env
     laya-env\Scripts\activate
     pip install torch --index-url https://download.pytorch.org/whl/cpu
     pip install laya

  4. Lance le tri :

     python trier_commentaires.py

  Au premier lancement le modèle multilingue se télécharge (environ 650 Mo).
  Ensuite tout fonctionne hors ligne.

  Pour taper tes propres commentaires en direct :

     python trier_commentaires.py --live

TES PROPRES COMMENTAIRES
  Ouvre commentaires.csv avec le Bloc-notes. Une ligne par commentaire :
     texte;attendu
  où « attendu » vaut idee_video, question, critique, compliment ou spam.
  Le score affiché à la fin compare les réponses de Laya à tes étiquettes.

LICENCE
  Laya est publié par Convai Innovations sous licence Apache 2.0.
  https://github.com/NandhaKishorM/laya
  Ce script est libre d'utilisation et de modification.
