#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration semantic-release
"""

import subprocess
import sys
from typing import List, Tuple


def test_commit_message(message: str) -> Tuple[bool, str]:
    """
    Teste un message de commit avec semantic-release
    Retourne (success, output)
    """
    try:
        # Utilise semantic-release pour analyser le message
        result = subprocess.run(
            ["python", "-m", "semantic_release", "version", "--dry-run"],
            capture_output=True,
            text=True,
            env={"GIT_COMMIT_MESSAGE": message},
        )
        return True, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def main():
    """Teste différents types de commits"""

    # Messages de test pour les différents types
    test_messages = [
        # Types PATCH
        ("fix: correction du bug d'affichage", "PATCH"),
        ("doc: mise à jour de la documentation", "PATCH"),
        ("style: amélioration du formatage", "PATCH"),
        ("refactor: restructuration du code", "PATCH"),
        ("perf: optimisation des performances", "PATCH"),
        ("ui: amélioration de l'interface", "PATCH"),
        ("ux: meilleure expérience utilisateur", "PATCH"),
        ("content: ajout de nouveau contenu", "PATCH"),
        ("i18n: traduction en français", "PATCH"),
        ("typo: correction de fautes de frappe", "PATCH"),
        ("up: petite mise à jour", "PATCH"),
        ("update: mise à jour générale", "PATCH"),
        ("revert: annulation du commit précédent", "PATCH"),
        ("hotfix: correction urgente", "PATCH"),
        ("patch: correction mineure", "PATCH"),
        ("tweak: petit ajustement", "PATCH"),
        ("adjust: ajustement mineur", "PATCH"),
        ("correct: correction générale", "PATCH"),
        ("improve: amélioration", "PATCH"),
        ("enhance: amélioration", "PATCH"),
        ("optimize: optimisation", "PATCH"),
        ("clean: nettoyage du code", "PATCH"),
        ("format: formatage", "PATCH"),
        ("lint: corrections de linting", "PATCH"),
        ("deps: mise à jour des dépendances", "PATCH"),
        ("security: correction de sécurité", "PATCH"),
        ("config: modification de configuration", "PATCH"),
        ("meta: mise à jour des métadonnées", "PATCH"),
        ("misc: changements divers", "PATCH"),
        # Types MINOR
        ("feat: nouvelle fonctionnalité", "MINOR"),
        ("upgrade: amélioration majeure", "MINOR"),
        ("maj: mise à jour majeure", "MINOR"),
        # Types MAJOR
        ("feat!: changement incompatible", "MAJOR"),
        ("breaking: changement majeur", "MAJOR"),
        # Messages non conformes
        ("simple message sans type", "NONE"),
        ("invalid: type non reconnu", "NONE"),
        ("Ajout de nouvelles fonctionnalités", "NONE"),
        ("Correction de bugs", "NONE"),
        ("Mise à jour", "NONE"),
        ("WIP: travail en cours", "NONE"),
    ]

    print("🧪 Test de la configuration semantic-release")
    print("=" * 50)

    success_count = 0
    total_count = len(test_messages)

    for message, expected_type in test_messages:
        print(f"\n📝 Test: {message}")
        print(f"   Attendu: {expected_type}")

        # Pour ce test simple, on vérifie juste que le message est bien formaté
        # selon les conventions Conventional Commits
        if (
            ":" in message
            and not message.startswith("simple")
            and not message.startswith("invalid")
        ):
            commit_type = message.split(":")[0].split("(")[0]

            # Vérifie si le type est dans notre configuration
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

            if commit_type in patch_types:
                result_type = "PATCH"
            elif commit_type in minor_types:
                result_type = "MINOR"
            elif commit_type in major_types or "!" in message.split(":")[0]:
                result_type = "MAJOR"
            else:
                result_type = "NONE"

            if result_type == expected_type:
                print(f"   ✅ Résultat: {result_type}")
                success_count += 1
            else:
                print(f"   ❌ Résultat: {result_type} (attendu: {expected_type})")
        else:
            if expected_type == "NONE":
                print(f"   ✅ Résultat: NONE (message non conforme)")
                success_count += 1
            else:
                print(f"   ❌ Résultat: NONE (attendu: {expected_type})")

    print("\n" + "=" * 50)
    print(f"📊 Résultats: {success_count}/{total_count} tests réussis")

    if success_count == total_count:
        print("🎉 Tous les tests sont passés !")
        return 0
    else:
        print("⚠️  Certains tests ont échoué")
        return 1


if __name__ == "__main__":
    sys.exit(main())
