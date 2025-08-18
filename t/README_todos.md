# Scanner de TODOs Personnalisés

Ce script scanne votre projet pour identifier tous vos tags TODO personnalisés et génère un rapport détaillé.

## 🏷️ Tags supportés (par ordre de priorité)

### 🚨 URGENT (à traiter en priorité)
- `2fix` - à solutionner (bugs critiques)
- `2ar` - à enlever (nettoyage nécessaire)

### ⚠️ IMPORTANT (à traiter rapidement)
- `2dbug` - oki2 (éléments à vérifier)
- `* [/]` - en cours (travail actuel)

### 📋 MOYEN (planification normale)
- `* [ ]` - à faire (tâches planifiées)
- `2do` - à faire (tâches générales)
- `2see` - à voir (à examiner)

### 💤 FAIBLE (peut attendre)
- `2let` - à laisser (non prioritaire)

## 🚀 Utilisation

### Utilisation simple
```bash
# Résumé rapide (recommandé pour usage quotidien)
python t/todos.py

# Scan complet avec détails
python t/scan_todos.py
```

### Options avancées
```bash
# Afficher seulement le résumé
python t/scan_todos.py --summary-only

# Filtrer par un tag spécifique
python t/scan_todos.py --tag "2fix"
python t/scan_todos.py --tag "* [ ]"

# Scanner un autre répertoire
python t/scan_todos.py --dir ../autre-projet

# Spécifier un fichier settings VSCode personnalisé
python t/scan_todos.py --settings /path/to/settings.json

# Mode debug (afficher les exclusions)
python t/scan_todos.py --debug
```

## 📊 Exemple de sortie

### Résumé rapide (`python t/todos.py`)
```text
📊 Résumé des TODOs par type :
+------------+--------+
| Tag        | Count  |
+------------+--------+
| 2fix       | 3      |
| 2ar        | 1      |
| 2dbug      | 2      |
| * [/]      | 1      |
| * [ ]      | 22     |
| 2do        | 1      |
| 2see       | 1      |
| 2let       | 1      |
+------------+--------+
| TOTAL      | 32     |
+------------+--------+
```

### Scan complet avec détails (`python t/scan_todos.py`)
```text
🚨 2fix (3 occurrences):
   📁 txt.md:7 → à solutioner
   📁 docs/divers/pain.md:38 → éviter dupli de ce bloc
   📁 docs/outils/technos/env/vsc/extensions.md:10 → just pour test

🚨 2ar (1 occurrence):
   📁 txt.md:9 → à enlever

⚠️ 2dbug (2 occurrences):
   📁 txt.md:8 → oki2
   📁 docs/outils/technos/env/vsc/extensions.md:9 → just pour test

📋 * [ ] (22 occurrences):
   📁 mkdocs.yml:192 → à tester git-revision-date-localized
   📁 txt.md:13 → à faire
   [... autres tâches ...]

💤 2let (1 occurrence):
   📁 txt.md:15 → à laisser
```

## 🔧 Configuration

### Extensions de fichiers scannées
Le script scanne automatiquement ces types de fichiers :
- Code : `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.html`, `.css`, `.php`, `.java`, `.c`, `.cpp`, etc.
- Documentation : `.md`, `.txt`
- Configuration : `.json`, `.yml`, `.yaml`, `.toml`, `.ini`, `.cfg`
- Scripts : `.sh`, `.bat`, `.ps1`

### Dossiers exclus par défaut
- `site/`, `.venv/`, `venv/`, `node_modules/`
- `.git/`, `__pycache__/`, `.pytest_cache/`
- `dist/`, `build/`, `.next/`, `.nuxt/`
- `coverage/`, fichiers minifiés

## 📝 Intégration VSCode

Le script peut utiliser votre configuration VSCode pour les exclusions :
- Lit automatiquement `%APPDATA%\Code\User\settings.json`
- Utilise les patterns `todo-tree.filtering.excludeGlobs`
- Combine avec les exclusions par défaut

## 🎯 Conseils d'utilisation par priorité

### 🚨 Workflow URGENT
1. **Matin** : `python t/todos.py` pour voir les priorités du jour
2. **Focus sur `2fix`** : Corriger les bugs critiques en premier
3. **Nettoyage `2ar`** : Supprimer le code obsolète rapidement

### ⚠️ Workflow IMPORTANT
4. **Vérification `2dbug`** : Tester les éléments marqués "oki2"
5. **Suivi `* [/]`** : Continuer le travail en cours

### 📋 Workflow MOYEN
6. **Planification `* [ ]`** : Organiser les tâches à faire
7. **Tâches `2do`** : Traiter les actions générales
8. **Examen `2see`** : Analyser les éléments à voir

### 💤 Workflow FAIBLE
9. **Archive `2let`** : Laisser pour plus tard

### 🔄 Conseils pratiques
- **Avant commit** : Vérifier qu'il ne reste pas de `2fix` ou `2ar`
- **Fin de journée** : Marquer les tâches terminées
- **Début de sprint** : Convertir les `* [ ]` en `* [/]` pour le travail en cours
