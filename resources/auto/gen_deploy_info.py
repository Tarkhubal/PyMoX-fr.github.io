#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime
import pytz
import argparse

# Parsing des arguments
parser = argparse.ArgumentParser(description="Génère le fichier deploy_info.md")
parser.add_argument(
    "--mode",
    choices=["manual", "cron", "hebdo"],
    default="manual",
    help="Mode de déploiement: manual (par défaut), cron (automatique quotidien), hebdo (rapport hebdomadaire)",
)
args = parser.parse_args()

DEPLOY_INFO_DIR = "docs/outils/logs"
DEPLOY_INFO_FILE = "deploy_info.md"
DEPLOY_INFO_PATH = os.path.join(DEPLOY_INFO_DIR, DEPLOY_INFO_FILE)

# SHA du commit actuel (ou depuis variable d'environnement)
SHA = (
    os.environ.get("SHA")
    or subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
)

# Dernier message de commit
LAST_COMMIT_MSG = subprocess.check_output(
    ["git", "log", "-1", "--pretty=%B"], text=True
).strip()

# Vérifie si le dernier commit est un merge vers github.io
if LAST_COMMIT_MSG.startswith("Merge") and "github.io" in LAST_COMMIT_MSG:
    PREV_SHA = subprocess.check_output(["git", "rev-parse", "HEAD^"], text=True).strip()

    MSG = (
        subprocess.check_output(
            ["git", "show", "-s", "--format=%B", PREV_SHA], text=True
        ).strip()
        + "<br>*([This commit has since been merged]"
    )
    MSG += "(https://github.com/PyMoX-fr/PyMoX-fr.github.io/commits/main))*"

    AUTOR = subprocess.check_output(
        ["git", "show", "-s", "--format=%an", PREV_SHA], text=True
    ).strip()

    commit_date_str = subprocess.check_output(
        ["git", "show", "-s", "--format=%ci", PREV_SHA], text=True
    ).strip()
else:
    MSG = LAST_COMMIT_MSG
    AUTOR = subprocess.check_output(
        ["git", "log", "-1", "--pretty=%an"], text=True
    ).strip()

    # Date actuelle si ce n'est pas un merge
    commit_date_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S +0000")

# Conversion des dates
commit_date = datetime.strptime(commit_date_str, "%Y-%m-%d %H:%M:%S %z")

# Europe/Paris
paris_tz = pytz.timezone("Europe/Paris")
date_human = commit_date.astimezone(paris_tz).strftime("%d/%m/%Y")
time_human = commit_date.astimezone(paris_tz).strftime("%H:%M:%S")

# UTC ISO 8601
date_iso = commit_date.astimezone(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

# UNIX timestamp
date_unix = int(commit_date.timestamp())

# Création du dossier
os.makedirs(DEPLOY_INFO_DIR, exist_ok=True)

# Définition des informations spécifiques au mode
mode_info = {
    "manual": {
        "title": "## → Suite à push manuel",
        "trigger": "🚀 **Déclencheur** : Push manuel sur la branche `main`",
        "footer": "> ✅ Ce déploiement a été lancé automatiquement suite au push manuel sur `main` "
        "(Sans commit permanent du fichier deploy-info.md dans l'historique Git).",
    },
    "cron": {
        "title": "## → Automatique (CRON quotidien)",
        "trigger": "🚀 **Déclencheur** : GitHub Actions (CRON quotidien)",
        "footer": "> ✅ Ce déploiement a été enclenché **automatiquement** comme chaque nuit vers 3h (G.M.T.).",
    },
    "hebdo": {
        "title": "## → Rapport Hebdomadaire",
        "trigger": "🚀 **Déclencheur** : GitHub Actions (Rapport Hebdomadaire)",
        "footer": "> ✅ Ce déploiement a été enclenché pour mettre à jour le rapport hebdomadaire.",
    },
}

# Sélection du mode
selected_mode = mode_info[args.mode]

# Écriture du fichier
with open(DEPLOY_INFO_PATH, "w", encoding="utf-8") as f:
    f.write("# 🚀 Dernier déploiement\n\n")
    f.write(f"{selected_mode['title']}\n\n")
    f.write(
        "| 📅 Date        | 🕰️ Heure (Paris)       | 🌐 ISO 8601 UTC         | 🔢 Timestamp UNIX |\n"
    )
    f.write(
        "|----------------|------------------------|------------------------|--------------------|\n"
    )
    f.write(
        f"| **{date_human}**  | **{time_human}**        | `{date_iso}`   | `{date_unix}`       |\n\n"
    )
    f.write("### 📋 Informations de déploiement\n\n")
    f.write(f"📝 Dernier commit (humain) : **{MSG}**<br>\n")
    f.write(f"👤 Auteur : {AUTOR}<br>\n")
    f.write(f"🔁 SHA Commit : `{SHA}`<br>\n")
    f.write(f"{selected_mode['trigger']}<br><br>\n")
    f.write(f"{selected_mode['footer']}\n")

print(f"✅ Fichier généré : {DEPLOY_INFO_PATH}")


# - name: 📋 Génère deploy_info.md
#   env:
#     SHA: ${{ github.sha }}
#   run: |
#     DEPLOY_INFO_DIR="docs/outils/logs"
#     DEPLOY_INFO_FILE="deploy_info.md"
#     DEPLOY_INFO_PATH="$DEPLOY_INFO_DIR/$DEPLOY_INFO_FILE"

#     mkdir -p "$DEPLOY_INFO_DIR"

#     LAST_COMMIT_MSG="$(git log -1 --pretty=%B)"

#     if [[ "$LAST_COMMIT_MSG" =~ ^Merge.*github\.io$ ]]; then

#       PREV_SHA="$(git rev-parse HEAD^)"
#       MSG="$(git show -s --format=%B "$PREV_SHA")<br>*([This commit has since been merged](https://github.com/PyMoX-fr/PyMoX-fr.github.io/commits/main))*"
#       AUTOR="$(git show -s --format=%an "$PREV_SHA")"

#       DATE_HUMAN="$(TZ='Europe/Paris' date -d "$(git show -s --format=%ci "$PREV_SHA")" '+%d/%m/%Y')"
#       TIME_HUMAN="$(TZ='Europe/Paris' date -d "$(git show -s --format=%ci "$PREV_SHA")" '+%H:%M:%S')"
#       DATE_ISO="$(date -u -d "$(git show -s --format=%ci "$PREV_SHA")" '+%Y-%m-%dT%H:%M:%SZ')"
#       DATE_UNIX="$(date -d "$(git show -s --format=%ci "$PREV_SHA")" '+%s')"

#       # # Fallback si MSG vide
#       # if [[ -z "$MSG" ]]; then
#       #   echo "⚠️ Le message du commit précédent est vide !"
#       #   MSG="[commit précédent vide ou inaccessible]"
#       # fi
#     else
#       MSG="$LAST_COMMIT_MSG"
#       AUTOR="$(git log -1 --pretty=%an)"
#       DATE_HUMAN="$(TZ='Europe/Paris' date '+%d/%m/%Y')"
#       TIME_HUMAN="$(TZ='Europe/Paris' date '+%H:%M:%S')"
#       DATE_ISO="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
#       DATE_UNIX="$(date +%s)"
#     fi

#     # SHA="${{ github.sha }}"

#     echo "" >> "$DEPLOY_INFO_PATH"

#     echo "# 🚀 Dernier déploiement" > "$DEPLOY_INFO_PATH"
#     echo "" >> "$DEPLOY_INFO_PATH"

#     echo "## → Suite à push manuel" >> "$DEPLOY_INFO_PATH"
#     echo "" >> "$DEPLOY_INFO_PATH"

#     echo "| 📅 Date        | 🕰️ Heure (Paris)       | 🌐 ISO 8601 UTC         | 🔢 Timestamp UNIX |" >> "$DEPLOY_INFO_PATH"
#     echo "|----------------|------------------------|------------------------|--------------------|" >> "$DEPLOY_INFO_PATH"
#     echo "| **$DATE_HUMAN**  | **$TIME_HUMAN**        | \`$DATE_ISO\`   | \`$DATE_UNIX\`       |" >> "$DEPLOY_INFO_PATH"
#     echo "" >> "$DEPLOY_INFO_PATH"

#     echo "### 📋 Informations de déploiement" >> "$DEPLOY_INFO_PATH"
#     echo "" >> "$DEPLOY_INFO_PATH"
#     echo "📝 Message Git : **${MSG}**<br>" >> "$DEPLOY_INFO_PATH"
#     echo "👤 Auteur : ${AUTOR}<br>" >> "$DEPLOY_INFO_PATH"
#     echo "🔁 SHA Commit : \`${SHA}\`<br>" >> "$DEPLOY_INFO_PATH"
#     echo "🚀 **Déclencheur** : Push manuel sur la branche \`main\`" >> "$DEPLOY_INFO_PATH"
#     echo "<br><br>" >> "$DEPLOY_INFO_PATH"

#     echo "> ✅ Ce déploiement a été lancé automatiquement suite au push manuel sur \`main\` (Sans commit permanent du fichier deploy-info.md dans l'historique Git)." >> "$DEPLOY_INFO_PATH"
