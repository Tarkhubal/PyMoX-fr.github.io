#!/usr/bin/env python3
"""
Script de raccourci pour scanner rapidement les TODOs.
Usage simple sans arguments pour un scan complet.
"""

import subprocess
import sys
import os

def main():
    # Chemin vers le script principal
    script_path = os.path.join(os.path.dirname(__file__), "scan_todos.py")
    
    if len(sys.argv) == 1:
        # Aucun argument : affichage résumé seulement
        subprocess.run([sys.executable, script_path, "--summary-only"])
    else:
        # Passer tous les arguments au script principal
        subprocess.run([sys.executable, script_path] + sys.argv[1:])

if __name__ == "__main__":
    main()
