import argparse, subprocess, shutil, os, pytz
from datetime import datetime
import tempfile

# Tester en dry-run :
#  python resources/auto/subs/push_reports.py --files CHANGELOG.md hebdo.md versions.json --ghref main --dry-run

# 🕒 Horodatage
paris_tz = pytz.timezone("Europe/Paris")
datehm = datetime.now(paris_tz).strftime("%Y-%m-%d %H:%M")

# 📁 Chemins
source = "docs/outils/logs/"
target = "reports"

# 🛠️ Arguments
parser = argparse.ArgumentParser(description="Push reports to gh-pages")
parser.add_argument(
    "--files", nargs="+", required=True, help="Liste des fichiers à sauvegarder"
)
parser.add_argument("--ghref", default="branche ?", help="Nom de la référence GH")
parser.add_argument("--dry-run", action="store_true", help="Simule sans exécuter")
parser.add_argument(
    "--keep-originals",
    action="store_true",
    help="Conserve les fichiers originaux après la copie (utile pour le workflow push.yml)",
)
args = parser.parse_args()

print(f"📄 Fichiers à traiter : {args.files}")
print(f"📝 Référence GitHub : {args.ghref}")

if args.dry_run:
    print("🧪 Mode simulation activé (dry-run)")

if args.keep_originals:
    print("📌 Conservation des fichiers originaux activée")


# 🧼 Commandes Git sécurisées
def run_git_command(cmd, allow_fail=False):
    if args.dry_run:
        print(f"🧪 [dry-run] Commande Git simulée : {' '.join(cmd)}")
        return True
    try:
        result = subprocess.run(
            cmd, check=not allow_fail, capture_output=True, text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git: {e}")
        if not allow_fail:
            exit(1)
        return False


# 📦 Utilisation d'un contexte de fichier temporaire pour éviter la gestion manuelle
with tempfile.TemporaryDirectory() as temp_dir:
    print(f"📁 Dossier temporaire créé: {temp_dir}")

    # 🔄 Collecte des fichiers à traiter
    files_to_process = {}

    # Traitement spécial pour versions.json
    versions_json_path = "docs/versions.json"
    if "versions.json" in args.files and os.path.exists(versions_json_path):
        files_to_process["versions.json"] = {
            "source": versions_json_path,
            "temp": os.path.join(temp_dir, "versions.json"),
            "target": os.path.join(target, "versions.json"),
        }
        print(f"✅ Fichier versions.json ajouté au traitement")

    # Traitement des autres fichiers
    for file in args.files:
        if file == "versions.json":
            continue

        source_path = os.path.join(source, file)
        if os.path.exists(source_path):
            files_to_process[file] = {
                "source": source_path,
                "temp": os.path.join(temp_dir, file),
                "target": os.path.join(target, file),
            }
            print(f"✅ Fichier {file} ajouté au traitement")
        else:
            print(f"⚠️ Fichier introuvable: {source_path}")

    # 📥 Copie des fichiers vers le dossier temporaire
    for file_name, paths in files_to_process.items():
        shutil.copy(paths["source"], paths["temp"])
        print(f"📦 Copié: {paths['source']} → {paths['temp']}")

    # 🧹 Nettoyage des fichiers originaux (sauf si --keep-originals est spécifié)
    if not args.keep_originals:
        for file_name, paths in files_to_process.items():
            if args.dry_run:
                print(f"🧪 [dry-run] Suppression simulée : {paths['source']}")
            else:
                try:
                    os.remove(paths["source"])
                    print(f"🧹 Supprimé: {paths['source']}")
                except Exception as e:
                    print(f"⚠️ Erreur lors de la suppression de {paths['source']}: {e}")
    else:
        print("📌 Conservation des fichiers originaux (--keep-originals activé)")

    # 🔄 Préparation de la branche gh-pages
    if not run_git_command(["git", "stash", "--include-untracked"]):
        print("⚠️ Problème lors du stash des modifications")

    run_git_command(["git", "fetch", "origin", "gh-pages"])

    if not run_git_command(["git", "switch", "gh-pages"]):
        print("❌ Impossible de basculer sur la branche gh-pages")
        exit(1)

    # 📁 Création du dossier cible
    os.makedirs(target, exist_ok=True)

    # 🚚 Copie des fichiers du dossier temporaire vers gh-pages/reports
    for file_name, paths in files_to_process.items():
        if args.dry_run:
            print(
                f"🧪 [dry-run] Déploiement simulé : {paths['temp']} → {paths['target']}"
            )
        else:
            shutil.copy(paths["temp"], paths["target"])
            print(f"📦 Déployé: {paths['temp']} → {paths['target']}")

    # 📤 Commit & push
    run_git_command(["git", "config", "user.name", "GitHub Actions"])
    run_git_command(["git", "config", "user.email", "actions@github.com"])
    run_git_command(["git", "add", target])

    commit_success = run_git_command(
        ["git", "commit", "-m", f"📄 Rapports de déploiement du {datehm}"],
        allow_fail=True,
    )

    if commit_success:
        # 🔐 Récupération sécurisée des variables GitHub
        github_token = os.environ.get("GITHUB_TOKEN", "TOKEN_INDISPONIBLE")
        github_repo = os.environ.get("GITHUB_REPOSITORY", "REPO_INDISPONIBLE")

        # ⚠️ Avertissement si les variables sont absentes en local
        if args.dry_run and (
            "TOKEN_INDISPONIBLE" in github_token or "REPO_INDISPONIBLE" in github_repo
        ):
            print(
                "⚠️  Variables GitHub non définies en local — simulation OK, mais PUSH RÉEL impossible, et NON SOUHAITÉ."
            )

        # 🔗 Configuration du remote
        run_git_command(
            [
                "git",
                "remote",
                "set-url",
                "origin",
                f"https://x-access-token:{github_token}@github.com/{github_repo}",
            ]
        )

        # 🚀 Push vers gh-pages
        run_git_command(["git", "push", "origin", "gh-pages"])
    else:
        print("ℹ️ Aucun changement à committer")

# 🔙 Retour sur main et restauration du stash
run_git_command(["git", "switch", "main"])
run_git_command(["git", "stash", "pop"], allow_fail=True)

print(
    "✅ Push terminé avec succès."
    if not args.dry_run
    else "🧪 Simulation terminée avec succès."
)
