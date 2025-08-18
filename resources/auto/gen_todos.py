#!/usr/bin/env python3
"""
Générateur de rapport TODO pour les workflows GitHub Actions.
Utilise scan_todos.py pour la logique de scan et génère le fichier todo.md.
"""

import os
import sys

# Ajouter le chemin vers le module scan_todos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "subs"))

from scan_todos import find_todos, generate_markdown_report


def main():
    """Génère le fichier todo.md pour les workflows."""
    print("🔍 Génération du rapport TODO pour le workflow...")

    # Scanner les todos dans le répertoire racine du projet
    root_dir = os.path.join(os.path.dirname(__file__), "../..")
    todos, counts = find_todos(root_dir, include_static_todo_md=True)

    # Générer le fichier todo.md dans docs/outils/logs/
    output_path = os.path.join(root_dir, "docs/outils/logs/todo.md")
    generate_markdown_report(todos, counts, output_path)

    print(f"✅ Rapport TODO généré avec succès : {output_path}")
    print(f"📊 Total: {sum(counts.values())} TODOs trouvés")


if __name__ == "__main__":
    main()
