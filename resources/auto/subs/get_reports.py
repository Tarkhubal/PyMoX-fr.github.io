import subprocess
import shutil
import os
import tempfile
import argparse


def run_git_command(cmd, allow_fail=False):
    """Exécute une commande git et retourne le résultat"""
    try:
        result = subprocess.run(
            cmd, check=not allow_fail, capture_output=True, text=True
        )
        return result.returncode == 0, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git: {e}")
        if not allow_fail:
            exit(1)
        return False, str(e)


def get_reports(files_to_get=None, dry_run=False):
    """
    Récupère les fichiers spécifiés depuis gh-pages/reports

    Args:
        files_to_get: Liste des fichiers à récupérer (par défaut: CHANGELOG.md et versions.json)
        dry_run: Si True, simule les opérations sans les exécuter
    """
    if files_to_get is None:
        files_to_get = ["CHANGELOG.md", "versions.json"]

    # Chemins de destination
    logs_dir = "docs/outils/logs"
    docs_dir = "docs"

    # Affichage des fichiers à récupérer
    print(
        f"📥 Récupération des fichiers depuis gh-pages/reports/: {', '.join(files_to_get)}"
    )

    # Vérification de l'existence de la branche gh-pages
    success, _ = run_git_command(["git", "fetch", "origin", "gh-pages"])
    if not success:
        print("⚠️ Impossible de récupérer la branche gh-pages")
        return False

    # Vérification de l'existence de la branche gh-pages
    success, output = run_git_command(
        ["git", "ls-remote", "--exit-code", "--heads", "origin", "gh-pages"],
        allow_fail=True,
    )

    if not success:
        print("⚠️ La branche gh-pages n'existe pas encore")
        return False

    # Utilisation d'un répertoire temporaire pour le worktree
    with tempfile.TemporaryDirectory() as tmp_dir:
        print(f"📁 Création d'un worktree temporaire dans {tmp_dir}")

        # Création du worktree
        success, _ = run_git_command(["git", "worktree", "add", tmp_dir, "gh-pages"])
        if not success:
            print("❌ Impossible de créer le worktree")
            return False

        # Traitement de chaque fichier
        files_processed = []

        for file_name in files_to_get:
            src_path = os.path.join(tmp_dir, "reports", file_name)

            # Déterminer le chemin de destination en fonction du fichier
            if file_name == "versions.json":
                dest_path = os.path.join(docs_dir, file_name)
            else:
                dest_path = os.path.join(logs_dir, file_name)

            # Vérifier si le fichier source existe
            if os.path.isfile(src_path):
                # Créer le répertoire de destination si nécessaire
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                if dry_run:
                    print(f"🧪 [dry-run] Copie simulée : {src_path} → {dest_path}")
                else:
                    # Copier le fichier
                    shutil.copy(src_path, dest_path)
                    print(f"✅ {file_name} copié dans {dest_path}")

                files_processed.append(file_name)
            else:
                print(f"⚠️ Fichier {file_name} non trouvé dans gh-pages/reports/")

        # Nettoyage du worktree
        print(f"🧹 Suppression du worktree temporaire")
        run_git_command(["git", "worktree", "remove", tmp_dir, "--force"])

        # Résumé
        if files_processed:
            print(
                f"✅ {len(files_processed)}/{len(files_to_get)} fichiers récupérés avec succès"
            )
        else:
            print("⚠️ Aucun fichier n'a pu être récupéré")

        return len(files_processed) > 0


if __name__ == "__main__":
    # Parsing des arguments
    parser = argparse.ArgumentParser(
        description="Récupérer des fichiers depuis gh-pages/reports"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        default=["CHANGELOG.md", "versions.json"],
        help="Liste des fichiers à récupérer",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Simule les opérations sans les exécuter"
    )
    args = parser.parse_args()

    # Exécution
    get_reports(args.files, args.dry_run)
