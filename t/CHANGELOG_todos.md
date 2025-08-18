# Changelog - Scanner de TODOs

## Version 2.0 - 2025-01-18 ✨

### 🎯 Nouvelles fonctionnalités majeures
- **Ordre de priorité intelligent** : Affichage par urgence/importance
- **Emojis visuels** : 🚨 Urgent, ⚠️ Important, 📋 Moyen, 💤 Faible
- **Correspondance parfaite** avec VSCode TODO Tree (32 TODOs)
- **Option `--debug`** : Affichage des exclusions pour le débogage

### 🔧 Améliorations techniques
- **Regex plus flexibles** : Détection améliorée des formats `* [ ]` et `* [/]`
- **Filtrage intelligent** : Exclusion automatique des faux positifs
- **Exclusions étendues** : Ignore les fichiers de résultats TODO Tree
- **Performance optimisée** : Scan plus rapide et précis

### 📊 Ordre de priorité implémenté
1. **🚨 URGENT** : `2fix` (bugs), `2ar` (nettoyage)
2. **⚠️ IMPORTANT** : `2dbug` (vérification), `* [/]` (en cours)
3. **📋 MOYEN** : `* [ ]` (tâches), `2do` (général), `2see` (examen)
4. **💤 FAIBLE** : `2let` (peut attendre)

### 📝 Documentation mise à jour
- Guide complet avec workflows par priorité
- Exemples de sortie avec nouveaux emojis
- Conseils d'utilisation optimisés pour la productivité

---

## Version 1.0 - 2025-01-18 🚀

### 🎉 Version initiale
- **8 tags personnalisés** supportés
- **30+ extensions** de fichiers scannées
- **Exclusions intelligentes** (site/, .venv/, etc.)
- **Intégration VSCode** settings.json
- **Options en ligne de commande** complètes
- **Script de raccourci** `todos.py`

### 🏷️ Tags supportés
- `2fix`, `2dbug`, `2ar`, `2see` (types personnalisés)
- `* [/]`, `* [ ]` (format markdown)
- `2do`, `2let` (tâches générales)

### 🚀 Fonctionnalités
- Scan récursif avec exclusions
- Filtrage par tag
- Résumé et détails
- Correspondance VSCode TODO Tree
