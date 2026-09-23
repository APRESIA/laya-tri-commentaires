# -*- coding: utf-8 -*-
"""
Trier ses commentaires YouTube avec Laya (open source, 100 % local).
L'Après IA — démo pour la vidéo « Laya : l'IA open source qui décide au lieu d'écrire ».

Utilisation :
    python trier_commentaires.py                  # trie commentaires.csv et donne le score
    python trier_commentaires.py --live           # puis tu tapes tes propres commentaires
    python trier_commentaires.py --fichier mes_commentaires.csv

Le fichier CSV : une ligne par commentaire, séparateur « ; »
    texte;attendu
    Super vidéo merci !;compliment
(la colonne « attendu » est facultative : si elle est remplie, le script calcule le taux de bonnes réponses)
"""
import argparse, csv, os, sys, time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
os.system("")  # active les couleurs dans l'invite de commandes Windows

G, R, Y, C, D, B, Z = "\033[92m", "\033[91m", "\033[93m", "\033[96m", "\033[90m", "\033[1m", "\033[0m"

# ---------------------------------------------------------------- les questions posées à Laya
# Laya ne rédige rien : il choisit parmi des réponses qu'on lui impose.
QUESTIONS = {
    "type": {
        "type": "choice",
        "instructions": "Quel type de commentaire YouTube est `texte` ?",
        "criteria": {
            "idee_video": "propose un sujet ou demande un épisode",
            "question": "pose une question au créateur",
            "critique": "critique négative de la vidéo ou du créateur",
            "compliment": "remerciement, encouragement ou félicitations",
            "spam": "arnaque, publicité, promesse d'argent ou lien suspect",
        },
    },
    "repondre": {
        "type": "noul",
        "instructions": "Le créateur de la vidéo devrait-il répondre à `texte` ?",
    },
    "ton": {
        "type": "score",
        "instructions": "Quel est le ton de `texte` ?",
        "criteria": ["très négatif", "négatif", "neutre", "positif", "très positif"],
    },
}
NOMS = {"idee_video": "IDÉE DE VIDÉO", "question": "QUESTION", "critique": "CRITIQUE",
        "compliment": "COMPLIMENT", "spam": "SPAM"}
COUL = {"idee_video": C, "question": Y, "critique": R, "compliment": G, "spam": R + B}


def court(t, n):
    t = " ".join(str(t).split())
    return t if len(t) <= n else t[: n - 1] + "…"


def lire(fichier):
    lignes = []
    with open(fichier, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            txt = (row.get("texte") or "").strip()
            if txt:
                lignes.append((txt, (row.get("attendu") or "").strip()))
    return lignes


def analyser(router, modele, texte):
    t = time.perf_counter()
    res = router.predict({"texte": texte}, QUESTIONS, model=modele)
    ms = (time.perf_counter() - t) * 1000
    a = res["answers"]
    return {
        "type": a["type"]["choice"],
        "type_conf": a["type"]["probabilities"][a["type"]["choice"]],
        "repondre": a["repondre"]["noul"],
        "ton": QUESTIONS["ton"]["criteria"][int(round(a["ton"]["score"]))],
        "ton_score": a["ton"]["score"],
        "ms": ms,
    }


def afficher(i, texte, r, attendu=""):
    typ = f"{COUL[r['type']]}{NOMS[r['type']]:<14}{Z}"
    conf = f"{D}{r['type_conf']*100:3.0f} %{Z}"
    rep = f"{G}répondre{Z}" if r["repondre"] >= 0.5 else f"{D}ignorer {Z}"
    verdict = ""
    if attendu:
        verdict = f"  {G}✓{Z}" if attendu == r["type"] else f"  {R}✗ (attendu : {NOMS.get(attendu, attendu)}){Z}"
    print(f"{D}{i:>2}{Z}  {court(texte, 46):<46}  {typ} {conf}  {rep}  {D}{r['ton']:<12}{Z} {D}{r['ms']:5.0f} ms{Z}{verdict}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fichier", default="commentaires.csv")
    ap.add_argument("--modele", default="multilingual", help="multilingual (français) ou english")
    ap.add_argument("--live", action="store_true", help="taper ses propres commentaires après le tri")
    args = ap.parse_args()

    print(f"\n{B}LAYA · tri de commentaires YouTube · 100 % local{Z}")
    print(f"{D}Chargement du modèle « {args.modele} » (la première fois : téléchargement d'environ 650 Mo)…{Z}")
    t0 = time.perf_counter()
    from laya import Router
    router = Router()
    analyser(router, args.modele, "échauffement")          # charge réellement le modèle
    print(f"{D}Modèle prêt en {time.perf_counter() - t0:.1f} s.{Z}\n")

    lignes = lire(args.fichier) if os.path.exists(args.fichier) else []
    resultats, ok, notes = [], 0, 0
    for i, (texte, attendu) in enumerate(lignes, 1):
        r = analyser(router, args.modele, texte)
        afficher(i, texte, r, attendu)
        resultats.append((texte, attendu, r))
        if attendu:
            notes += 1
            ok += attendu == r["type"]

    if resultats:
        moy = sum(r["ms"] for *_, r in resultats) / len(resultats)
        print(f"\n{B}{len(resultats)} commentaires triés{Z} · {moy:.0f} ms en moyenne par commentaire (3 questions à chaque fois)")
        if notes:
            print(f"{B}Bonnes réponses sur le type : {ok}/{notes} ({ok/notes*100:.0f} %){Z}")
        with open("resultats.csv", "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["texte", "attendu", "type_laya", "confiance", "a_repondre", "ton", "ms"])
            for texte, attendu, r in resultats:
                w.writerow([texte, attendu, r["type"], f"{r['type_conf']:.2f}", f"{r['repondre']:.2f}", r["ton"], f"{r['ms']:.0f}"])
        print(f"{D}Détail enregistré dans resultats.csv{Z}")

    if args.live:
        print(f"\n{B}À toi : écris un commentaire (Entrée sur une ligne vide pour quitter).{Z}")
        n = len(resultats)
        while True:
            try:
                texte = input(f"{C}> {Z}").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not texte:
                break
            n += 1
            afficher(n, texte, analyser(router, args.modele, texte))
    print()


if __name__ == "__main__":
    main()
