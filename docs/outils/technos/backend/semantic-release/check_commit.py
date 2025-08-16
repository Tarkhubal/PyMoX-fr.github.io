#!/usr/bin/env python3
"""
Script utilitaire pour vérifier si un message de commit déclenchera une nouvelle version
"""

import sys
import re
from typing import Optional, Tuple


def analyze_commit_message(message: str) -> Tuple[Optional[str], str, str]:
    """
    Analyse un message de commit et détermine le type de version

    Returns:
        (version_type, commit_type, description)
    """

    # Configuration des types (synchronisée avec pyproject.toml)
    patch_types = [
        "fix",
        "doc",
        "style",
        "refactor",
        "perf",
        "ui",
        "ux",
        "content",
        "i18n",
        "typo",
        "up",
        "update",
        "revert",
        "hotfix",
        "patch",
        "tweak",
        "adjust",
        "correct",
        "improve",
        "enhance",
        "optimize",
        "clean",
        "format",
        "lint",
        "deps",
        "security",
        "config",
        "meta",
        "misc",
    ]
    minor_types = ["feat", "maj", "upgrade"]
    major_types = ["breaking"]

    # Pattern pour Conventional Commits
    pattern = r"^(?P<type>[a-zA-Z]+)(?:\((?P<scope>[^\)]+)\))?(?P<breaking>!)?: (?P<description>.+)"

    match = re.match(pattern, message.strip())

    if not match:
        return None, "INVALID", "Message ne respecte pas le format Conventional Commits"

    commit_type = match.group("type")
    scope = match.group("scope") or ""
    breaking = bool(match.group("breaking"))
    description = match.group("description")

    # Détermine le type de version
    if breaking or commit_type in major_types:
        version_type = "MAJOR"
    elif commit_type in minor_types:
        version_type = "MINOR"
    elif commit_type in patch_types:
        version_type = "PATCH"
    else:
        version_type = None

    return version_type, commit_type, description


def main():
    """Interface en ligne de commande"""

    if len(sys.argv) < 2:
        print('Usage: python check_commit.py "message de commit"')
        print("\nExemples:")
        print('  python check_commit.py "fix: correction du bug d\'affichage"')
        print('  python check_commit.py "feat: nouvelle fonctionnalité"')
        print('  python check_commit.py "docs: mise à jour de la documentation"')
        return 1

    message = " ".join(sys.argv[1:])

    print(f"📝 Message de commit: {message}")
    print("-" * 50)

    version_type, commit_type, description = analyze_commit_message(message)

    if commit_type == "INVALID":
        print("❌ Message invalide")
        print(f"   Raison: {description}")
        print("\n💡 Format attendu: type(scope): description")
        print("   Exemples: fix: correction du bug")
        print("            feat(api): nouvelle fonctionnalité")
        print("            docs: mise à jour documentation")
        return 1

    print(f"✅ Type de commit: {commit_type}")
    print(f"📄 Description: {description}")

    if version_type:
        print(f"🔢 Impact sur la version: {version_type}")

        if version_type == "PATCH":
            print("   → Incrémente la version patch (0.0.X)")
        elif version_type == "MINOR":
            print("   → Incrémente la version mineure (0.X.0)")
        elif version_type == "MAJOR":
            print("   → Incrémente la version majeure (X.0.0)")
    else:
        print("⚠️  Ce type de commit ne déclenchera PAS de nouvelle version")
        print(f"   Le type '{commit_type}' n'est pas reconnu dans la configuration")

    return 0


if __name__ == "__main__":
    sys.exit(main())
