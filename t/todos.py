#!/usr/bin/env python3
"""
Script de raccourci pour scanner rapidement les TODOs.
Usage simple sans arguments pour un scan complet.
Utilise maintenant resources/auto/subs/scan_todos.py pour la logique.
"""

import sys
import os, pytz

# Ajouter le chemin vers le module scan_todos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../resources/auto/subs"))

from scan_todos import find_todos, print_results


def main():
    """Affiche les todos trouvés dans le projet dans la console."""
    print("🔍 Scan des TODOs dans le projet...")
    print(f"📂 Répertoire: {os.path.abspath('.')}")
    print()

    # Utiliser la fonction find_todos du module scan_todos avec inclusion du TODO statique
    todos, counts = find_todos(".", include_static_todo_md=True)

    # Afficher les résultats dans la console
    print_results(todos, counts)


if __name__ == "__main__":
    main()
