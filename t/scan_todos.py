import os
import re
import fnmatch
import argparse
from collections import defaultdict

# Extensions de fichiers à scanner (élargi selon votre demande)
SCAN_EXT = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".html",
    ".css",
    ".scss",
    ".sass",
    ".md",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
    ".sh",
    ".bat",
    ".ps1",
    ".php",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".go",
    ".rs",
    ".rb",
    ".swift",
    ".kt",
    ".dart",
    ".vue",
    ".svelte",
}

# Dossiers et fichiers à ignorer par défaut
DEFAULT_EXCLUDES = [
    "site/**",
    ".venv/**",
    "venv/**",
    "node_modules/**",
    ".git/**",
    "__pycache__/**",
    "*.pyc",
    ".pytest_cache/**",
    "dist/**",
    "build/**",
    ".next/**",
    ".nuxt/**",
    "coverage/**",
    ".coverage/**",
    "*.min.js",
    "*.min.css",
    # Exclure les fichiers de ce script et sa documentation
    "t/scan_todos.py",
    "t/todos.py",
    "t/README_todos.md",
    "t/CHANGELOG_todos.md",
    # Exclure les fichiers de résultats TODO Tree
    "todo-tree*.txt",
]

# Tags selon votre liste exacte avec regex plus flexibles
TAGS = {
    "2fix": r"(?:^|[^a-zA-Z0-9])2fix\b(.*)$",  # à solutionner
    "2dbug": r"(?:^|[^a-zA-Z0-9])2dbug\b(.*)$",  # oki2
    "2ar": r"(?:^|[^a-zA-Z0-9])2ar\b(.*)$",  # à enlever
    "2see": r"(?:^|[^a-zA-Z0-9])2see\b(.*)$",  # à voir
    "* [/]": r".*\*\s*\[/\]\s*(.*)$",  # en cours (plus flexible)
    "* [ ]": r".*\*\s*\[\s*\]\s*(.*)$",  # à faire (plus flexible)
    "2do": r"(?:^|[^a-zA-Z0-9])2do\b(.*)$",  # à faire
    "2let": r"(?:^|[^a-zA-Z0-9])2let\b(.*)$",  # à laisser
}

TAG_REGEXES = {k: re.compile(v, re.IGNORECASE | re.MULTILINE) for k, v in TAGS.items()}

# Ordre de priorité pour l'affichage (du plus urgent au moins urgent)
PRIORITY_ORDER = [
    "2fix",  # URGENT - à solutionner (bugs)
    "2ar",  # URGENT - à enlever (nettoyage)
    "2dbug",  # IMPORTANT - oki2 (à vérifier)
    "* [/]",  # IMPORTANT - en cours (travail actuel)
    "* [ ]",  # MOYEN - à faire (tâches planifiées)
    "2do",  # MOYEN - à faire (tâches générales)
    "2see",  # MOYEN - à voir (à examiner)
    "2let",  # FAIBLE - à laisser (peut attendre)
]


def load_excludes(settings_path):
    """Récupère la liste des excludeGlobs sans parser tout le settings.json."""
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(
            r'"todo-tree\.filtering\.excludeGlobs"\s*:\s*\[(.*?)\]', content, re.S
        )
        if not match:
            print("ℹ️ Aucun excludeGlobs trouvé dans settings.json")
            return []

        raw_array = match.group(1)
        excludes = re.findall(r'"([^"]+)"', raw_array)
        print(f"ℹ️ Exclusions chargées depuis VSCode : {excludes}")
        return excludes

    except Exception as e:
        print(f"⚠️ Impossible de lire {settings_path} : {e}")
        return []


def is_excluded(path, exclude_globs):
    for pattern in exclude_globs:
        if fnmatch.fnmatch(path.replace("\\", "/"), pattern):
            return True
    return False


def find_todos(root=".", settings_path=None):
    todos = []
    counts = defaultdict(int)

    # Utiliser les exclusions par défaut + celles de VSCode si disponibles
    exclude_globs = DEFAULT_EXCLUDES.copy()
    if settings_path:
        vscode_excludes = load_excludes(settings_path)
        exclude_globs.extend(vscode_excludes)

    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace("\\", "/")

        # Exclure certains sous-dossiers pour la descente
        dirnames[:] = [
            d
            for d in dirnames
            if not is_excluded(
                os.path.join(rel_dir, d).replace("\\", "/") + "/", exclude_globs
            )
        ]

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            rel_file = os.path.relpath(filepath, root).replace("\\", "/")

            if is_excluded(rel_file, exclude_globs):
                continue

            ext = os.path.splitext(filename)[1].lower()
            if ext not in SCAN_EXT:
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, start=1):
                        # Ignorer les lignes de code/exemples qui ne sont pas de vrais TODOs
                        line_lower = line.lower().strip()

                        # Ignorer seulement les lignes qui sont clairement des exemples de documentation
                        if any(
                            skip in line_lower
                            for skip in [
                                "python scan_todos",
                                "| tag",
                                "+-",
                                'r".*',  # Regex dans le code (plus spécifique)
                                "r'.*",  # Regex dans le code (plus spécifique)
                                "tags recherchés",
                                "afficher seulement",
                                ": 4 ,",  # Ligne de comptage dans txt.md
                                "1 dbug, 1 2ar",  # Ligne de comptage
                            ]
                        ):
                            continue

                        # Ignorer les lignes dans des blocs de code markdown (mais pas les commentaires HTML)
                        if line.strip().startswith("```"):
                            continue

                        for tag, regex in TAG_REGEXES.items():
                            match = regex.search(line)
                            if match:
                                # Extraire le texte qui suit le tag
                                tag_text = (
                                    match.group(1).strip() if match.groups() else ""
                                )
                                full_text = line.strip()

                                todos.append(
                                    {
                                        "file": rel_file,
                                        "line": i,
                                        "text": full_text,
                                        "tag": tag,
                                        "tag_text": tag_text,
                                    }
                                )
                                counts[tag] += 1
                                break
            except Exception as e:
                print(f"⚠️ Impossible de lire {filepath} : {e}")

    return todos, counts


def print_results(todos, counts):
    """Affiche les résultats de manière claire et organisée."""
    if not todos:
        print("✅ Aucun TODO trouvé dans le projet")
        return

    print(f"📌 {len(todos)} TODOs trouvés dans le projet :\n")

    # Grouper par tag pour un affichage organisé
    todos_by_tag = defaultdict(list)
    for todo in todos:
        todos_by_tag[todo["tag"]].append(todo)

    # Afficher chaque tag avec ses occurrences dans l'ordre de priorité
    for tag in PRIORITY_ORDER:
        if tag in todos_by_tag:
            tag_todos = todos_by_tag[tag]
            # Emoji selon la priorité
            if tag in ["2fix", "2ar"]:
                emoji = "🚨"  # URGENT
            elif tag in ["2dbug", "* [/]"]:
                emoji = "⚠️"  # IMPORTANT
            elif tag in ["* [ ]", "2do", "2see"]:
                emoji = "📋"  # MOYEN
            else:
                emoji = "💤"  # FAIBLE

            print(
                f"{emoji} {tag} ({len(tag_todos)} occurrence{'s' if len(tag_todos) > 1 else ''}):"
            )

            for todo in tag_todos:
                tag_text = todo["tag_text"]
                if tag_text:
                    print(f"   📁 {todo['file']}:{todo['line']} → {tag_text}")
                else:
                    print(f"   📁 {todo['file']}:{todo['line']} → {todo['text']}")
            print()

    # Ligne de séparation
    print("=" * 60)
    print()

    # Tableau résumé par tag
    print("📊 Résumé des TODOs par type :")
    print("+" + "-" * 12 + "+" + "-" * 8 + "+")
    print("| Tag        | Count  |")
    print("+" + "-" * 12 + "+" + "-" * 8 + "+")

    # Afficher dans l'ordre de priorité
    for tag in PRIORITY_ORDER:
        if tag in counts:
            count = counts[tag]
            print(f"| {tag:<10} | {count:<6} |")

    print("+" + "-" * 12 + "+" + "-" * 8 + "+")
    print(f"| {'TOTAL':<10} | {sum(counts.values()):<6} |")
    print("+" + "-" * 12 + "+" + "-" * 8 + "+")


def main():
    parser = argparse.ArgumentParser(
        description="Scanner de TODOs personnalisés dans un projet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python scan_todos.py                    # Scan du répertoire courant
  python scan_todos.py --dir ../autre     # Scan d'un autre répertoire
  python scan_todos.py --summary-only     # Afficher seulement le résumé
  python scan_todos.py --tag 2fix         # Afficher seulement les tags 2fix
        """,
    )

    parser.add_argument(
        "--dir",
        "-d",
        default=".",
        help="Répertoire à scanner (défaut: répertoire courant)",
    )

    parser.add_argument(
        "--summary-only",
        "-s",
        action="store_true",
        help="Afficher seulement le tableau résumé",
    )

    parser.add_argument("--tag", "-t", help="Filtrer par un tag spécifique")

    parser.add_argument("--settings", help="Chemin vers settings.json de VSCode")

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Afficher les informations de debug (fichiers exclus, etc.)",
    )

    args = parser.parse_args()

    # Chemin vers les settings VSCode (optionnel)
    settings_path = (
        args.settings or r"C:\Users\utilisateur\AppData\Roaming\Code\User\settings.json"
    )

    if not args.summary_only:
        print("🔍 Scan des TODOs dans le projet...")
        print(f"📂 Répertoire: {os.path.abspath(args.dir)}")
        print(f"🏷️  Tags recherchés: {', '.join(TAGS.keys())}")
        if args.tag:
            print(f"🎯 Filtrage par tag: {args.tag}")
        if args.debug:
            print(f"🚫 Exclusions: {', '.join(DEFAULT_EXCLUDES)}")
        print()

    # Vérifier si le fichier settings existe
    if os.path.exists(settings_path):
        todos, counts = find_todos(args.dir, settings_path)
    else:
        if not args.summary_only:
            print(f"ℹ️  Settings VSCode non trouvé: {settings_path}")
            print("ℹ️  Utilisation des exclusions par défaut uniquement")
        todos, counts = find_todos(args.dir)

    # Filtrer par tag si demandé
    if args.tag:
        todos = [t for t in todos if t["tag"] == args.tag]
        counts = {k: v for k, v in counts.items() if k == args.tag}

    if args.summary_only:
        # Afficher seulement le tableau
        if counts:
            print("📊 Résumé des TODOs par type :")
            print("+" + "-" * 12 + "+" + "-" * 8 + "+")
            print("| Tag        | Count  |")
            print("+" + "-" * 12 + "+" + "-" * 8 + "+")

            for tag in PRIORITY_ORDER:
                if tag in counts:
                    count = counts[tag]
                    print(f"| {tag:<10} | {count:<6} |")

            print("+" + "-" * 12 + "+" + "-" * 8 + "+")
            print(f"| {'TOTAL':<10} | {sum(counts.values()):<6} |")
            print("+" + "-" * 12 + "+" + "-" * 8 + "+")
        else:
            print("✅ Aucun TODO trouvé")
    else:
        print_results(todos, counts)


if __name__ == "__main__":
    main()
