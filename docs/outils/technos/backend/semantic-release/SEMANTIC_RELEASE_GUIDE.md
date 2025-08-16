# Guide Semantic Release pour PyMoX

Ce guide explique comment utiliser la configuration semantic-release étendue pour automatiser le versioning de votre site MkDocs.

## 🎯 Objectif

Permettre l'incrémentation automatique de version (patch) avec une variété de mots-clés au-delà du simple `fix:`, adaptés aux besoins d'un site de documentation.

## ⚙️ Configuration

La configuration se trouve dans `pyproject.toml` :

```toml
  [tool.semantic_release]
  version_source = "tag"
  branch = "main"
  upload_to_pypi = false
  commit_parser = "angular"
  
  [tool.semantic_release.commit_parser_options]
  # Types qui déclenchent une version MINEURE (0.x.0)
  minor_tags = ["feat", "maj", "upgrade"]
  
  # Types qui déclenchent une version PATCH (0.0.x)
  patch_tags = [
      "fix", "doc", "style", "refactor", "perf", "ui", "ux",
      "content", "i18n", "typo", "up", "update", "revert", "hotfix",
      "patch", "tweak", "adjust", "correct", "improve", "enhance",
      "optimize", "clean", "format", "lint", "deps", "security",
      "config", "meta", "misc"
  ]
  
  # Types autorisés mais qui ne déclenchent pas de version
  other_allowed_tags = []
  
  # Liste complète de tous les types autorisés
  allowed_tags = [
      "feat", "maj", "upgrade",
      "fix", "doc", "style", "refactor", "perf", "ui", "ux",
      "content", "i18n", "typo", "up", "update", "revert", "hotfix",
      "patch", "tweak", "adjust", "correct", "improve", "enhance",
      "optimize", "clean", "format", "lint", "deps", "security",
      "config", "meta", "misc"
  ]
```

**Note importante :** Nous utilisons le parser `angular` car il supporte les types personnalisés via `patch_tags` et `minor_tags`. Le parser `conventional` ne permet pas d'ajouter des types personnalisés.

## 🚀 Utilisation

### Types de commits qui déclenchent une version PATCH (0.0.X)

#### Corrections et améliorations
- `fix:` - Correction de bug
- `hotfix:` - Correction urgente
- `patch:` - Correction mineure
- `correct:` - Correction générale
- `revert:` - Annulation d'un changement

#### Performance et optimisation
- `perf:` - Amélioration de performance
- `optimize:` - Optimisation du code
- `enhance:` - Amélioration générale

#### Interface et expérience
- `ui:` - Modifications de l'interface
- `ux:` - Améliorations UX
- `tweak:` - Petits ajustements
- `adjust:` - Ajustements mineurs

#### Contenu et documentation
- `doc:` - Documentation
- `content:` - Contenu du site
- `i18n:` - Traductions
- `typo:` - Fautes de frappe

#### Maintenance et outils
- `deps:` - Dépendances
- `security:` - Sécurité
- `config:` - Configuration
- `clean:` - Nettoyage
- `format:` - Formatage
- `lint:` - Linting
- `meta:` - Métadonnées
- `misc:` - Divers

#### Mises à jour
- `up:` - Petites mises à jour
- `update:` - Mises à jour générales

### Commits qui ne déclenchent PAS de version

**Tout commit sans format `type:`** ne déclenche aucune nouvelle version.

Exemples :
```bash
git commit -m "Ajout de nouvelles fonctionnalités"
git commit -m "Correction de bugs"
git commit -m "WIP: travail en cours"
git commit -m "Tests ajoutés"
git commit -m "Refactoring du code"
```

**Principe :** Si vous ne voulez pas déclencher de version, n'utilisez simplement pas le format `type: description`.

## 🧪 Tests

### Script de test complet
```bash
python test_semantic_release.py
```

### Vérification d'un message spécifique
```bash
python check_commit.py "typo: correction des fautes dans le README"
python check_commit.py "optimize: amélioration des performances"
python check_commit.py "deps: mise à jour de Material for MkDocs"
```

## 📝 Exemples pratiques

### Corrections de contenu
```bash
git commit -m "typo: correction des fautes dans la page d'accueil"
git commit -m "content: ajout de nouveaux exemples Python"
git commit -m "i18n: traduction de la section API"
git commit -m "doc: mise à jour de la documentation API"
```

### Améliorations techniques
```bash
git commit -m "optimize: amélioration des temps de chargement"
git commit -m "perf: optimisation des images"
git commit -m "clean: suppression du code mort"
```

### Maintenance
```bash
git commit -m "deps: mise à jour de Material for MkDocs vers v9.5.0"
git commit -m "config: amélioration de la configuration MkDocs"
git commit -m "security: correction de vulnérabilité"
```

### Interface utilisateur
```bash
git commit -m "ui: amélioration du contraste des boutons"
git commit -m "ux: simplification de la navigation"
git commit -m "tweak: ajustement de l'espacement"
```

## 🔄 Workflow GitHub Actions

Le workflow `.github/workflows/push.yml` utilise cette configuration :

```yaml
  - name: Run python-semantic-release
    env:
      GH_TOKEN: ${ { secrets.GITHUB_TOKEN }} # un espace à ôter ici { {
    run: |
      python -m semantic_release version
      python -m semantic_release publish
```

## 📊 Impact sur le versioning

- **MAJOR (X.0.0)** : `feat!:`, `breaking:`, ou commits avec `BREAKING CHANGE:`
- **MINOR (0.X.0)** : `feat:`, `upgrade:`, `maj:`
- **PATCH (0.0.X)** : Tous les autres types listés ci-dessus

## 💡 Conseils

1. **Format strict** : Respectez le format `type: description`
2. **Descriptions claires** : Utilisez des descriptions explicites
3. **Scope optionnel** : Vous pouvez ajouter un scope : `docs(api): mise à jour`
4. **Cohérence** : Utilisez toujours le même type pour des changements similaires

## 🔍 Vérification avant commit

Avant de faire un commit, vous pouvez vérifier son impact :

```bash
  python check_commit.py "votre message de commit"
```

Cela vous indiquera si le commit déclenchera une nouvelle version et de quel type.
