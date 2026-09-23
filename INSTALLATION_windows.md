# Installer Laya sur Windows et lancer la démo

Compte 15 minutes la première fois, dont une bonne partie de téléchargement. Pas besoin de carte graphique : Laya tourne sur le processeur.

## 1. Installer Python (une seule fois)

1. Va sur **python.org → Downloads → Windows** et télécharge **Python 3.12** (installateur 64 bits).
2. Au premier écran de l'installation, **coche « Add python.exe to PATH »**, puis *Install Now*.
3. Vérifie : ouvre l'invite de commandes et tape `py --version`. Tu dois voir `Python 3.12.x`.

## 2. Préparer le dossier de la démo

1. Ouvre le dossier `video-laya\demo` dans l'Explorateur.
2. Clique dans la barre d'adresse, tape `cmd` puis Entrée : une invite de commandes s'ouvre directement dans ce dossier.
3. Crée un environnement isolé (ça n'abîme rien sur ton PC) :

```
py -3.12 -m venv laya-env
laya-env\Scripts\activate
```

Le début de la ligne affiche maintenant `(laya-env)`.

## 3. Installer Laya

```
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install laya
```

La première ligne installe la version « processeur » de PyTorch, plus légère. La seconde installe Laya (licence Apache 2.0, par Convai Innovations).

## 4. Lancer la démo

```
python trier_commentaires.py
```

- **Au premier lancement**, le modèle multilingue (celui qui comprend le français) se télécharge depuis Hugging Face : environ 650 Mo. Ensuite il reste sur ton PC et tout fonctionne hors ligne.
- Le script trie les 20 commentaires de `commentaires.csv`, affiche pour chacun le type, la confiance, « répondre / ignorer », le ton et le temps de calcul. À la fin, il donne **le taux de bonnes réponses** et enregistre le détail dans `resultats.csv`.

Pour taper tes propres commentaires en direct après le tri :

```
python trier_commentaires.py --live
```

## 5. Le test sur tes vrais commentaires (le meilleur moment de la vidéo)

1. Dans YouTube Studio → **Commentaires**, copie 20 à 30 vrais commentaires.
2. Colle-les dans `commentaires.csv` (ouvre-le avec le Bloc-notes), une ligne par commentaire, sous la forme `texte;attendu`.
3. Dans la colonne `attendu`, mets ta propre réponse : `idee_video`, `question`, `critique`, `compliment` ou `spam`.
4. Relance `python trier_commentaires.py`. Le score affiché est **ton vrai résultat**, c'est lui qu'on annoncera dans la vidéo.

Si un commentaire contient un point-virgule, remplace-le par une virgule.

## Si ça coince

| Problème | Solution |
|---|---|
| `py` n'est pas reconnu | Réinstalle Python en cochant « Add python.exe to PATH ». |
| `activate` refusé dans PowerShell | Utilise l'invite de commandes (`cmd`), pas PowerShell. |
| Le téléchargement du modèle échoue | Vérifie ta connexion, relance : il reprend là où il s'était arrêté. |
| Accents bizarres dans la console | Utilise le **Terminal Windows** (installé par défaut sur Windows 11). |
| Tout est très lent la première fois | Normal : le chargement initial prend plusieurs secondes. Les commentaires suivants passent en une fraction de seconde. |

Espace disque nécessaire : environ 2 Go (PyTorch + le modèle).

## Pour filmer l'écran

- **OBS Studio**, en 1920 × 1080, le Terminal Windows en thème sombre et en **police de taille 20** pour que ce soit lisible sur un téléphone.
- Filme deux prises séparées : `capture_installation.mp4` (étapes 2 à 4) et `capture_demo.mp4` (le tri puis le mode `--live`).
- Coupe les attentes de téléchargement au montage. Garde en revanche le vrai temps d'affichage des résultats : la vitesse fait partie de la démonstration.
