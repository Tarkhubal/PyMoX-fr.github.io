# Types de Commits pour PyMoX

Ce document décrit les différents types de commits que vous pouvez utiliser dans ce projet et leur impact sur la versionnage sémantique.

## Types de Commits et Versionnage

### Déclenchent une version MAJEURE (x.0.0)

- `feat!:` - Nouvelle fonctionnalité avec changement incompatible
- Tout commit avec `BREAKING CHANGE:` dans le corps du message

### Déclenchent une version MINEURE (0.x.0)
- `feat:` - Nouvelle fonctionnalité
- `upgrade:` - Amélioration d'une fonctionnalité existante
- `maj:` - Mise à jour majeure (mais pas incompatible)

### Déclenchent une version PATCH (0.0.x)

#### Corrections et améliorations
- `fix:` - Correction de bug
- `hotfix:` - Correction urgente
- `patch:` - Correction mineure
- `correct:` - Correction générale
- `revert:` - Annulation d'un changement précédent

#### Performance et optimisation
- `perf:` - Amélioration de performance
- `optimize:` - Optimisation du code
- `enhance:` - Amélioration générale

#### Code et structure
- `refactor:` - Refactorisation qui ne change pas le comportement
- `style:` - Changements de formatage (espaces, indentation, etc.)
- `clean:` - Nettoyage du code
- `format:` - Formatage du code
- `lint:` - Corrections de linting

#### Interface et expérience utilisateur
- `ui:` - Modifications de l'interface utilisateur
- `ux:` - Améliorations de l'expérience utilisateur
- `tweak:` - Petits ajustements d'interface
- `adjust:` - Ajustements mineurs

#### Contenu et documentation
- `doc:` - Changements dans la documentation
- `content:` - Mise à jour du contenu
- `i18n:` - Internationalisation et traductions
- `typo:` - Correction de fautes de frappe

#### Mises à jour et maintenance
- `up:` - Petites mises à jour
- `update:` - Mises à jour générales
- `deps:` - Mise à jour des dépendances
- `security:` - Corrections de sécurité
- `config:` - Modifications de configuration
- `meta:` - Métadonnées et informations du projet
- `misc:` - Divers changements mineurs

### Ne déclenchent PAS de nouvelle version

**Tout commit sans format `type:`** ne déclenche aucune nouvelle version.

Exemples :
- `Ajout de nouvelles fonctionnalités`
- `Correction de bugs`
- `Mise à jour`
- `WIP: travail en cours`
- `Refactoring du code`
- `Tests ajoutés`

**Principe :** Si vous ne voulez pas déclencher de version, n'utilisez simplement pas le format `type: description`.

## Exemples d'utilisation

```git
feat: ajout d'une nouvelle fonctionnalité de recherche
```

```git
fix: correction du problème d'affichage sur mobile
```

```git
doc: mise à jour du guide d'installation
```

```git
feat!: refonte complète de l'API

BREAKING CHANGE: L'ancienne API n'est plus compatible
```

```git
improvement: optimisation des performances de chargement
```

```git
content: ajout de nouveaux exemples dans la documentation
```

```git
ui: amélioration du contraste des boutons
```

```git
i18n: ajout de la traduction en espagnol
```

```git
typo: correction des fautes dans la page d'accueil
```

```git
optimize: amélioration des temps de chargement
```

```git
config: mise à jour de la configuration MkDocs
```

```git
deps: mise à jour de Material for MkDocs vers v9.5.0
```

```git
security: correction de vulnérabilité dans les dépendances
```

```git
clean: suppression du code mort dans les templates
```

```git
hotfix: correction urgente du lien cassé en production
```

## Conseils pour de bons messages de commit

1. Utilisez l'impératif présent : "add" plutôt que "added"
2. Ne mettez pas de point à la fin de la première ligne
3. Limitez la première ligne à 72 caractères
4. Après la première ligne, ajoutez une ligne vide puis une description détaillée si nécessaire
5. Utilisez des listes à puces dans la description si approprié

## Les différents types de commits

| Emoji | Sens                           | Usage suggéré                             |
|-------|--------------------------------|-------------------------------------------|
| 🕒    | Dernières modifications        | "Last commits" chronologiques             |
| 📦    | Livraison de code              | Commit d’une feature ou d’un fix          |
| 🧠    | Travail réfléchi ou complexe   | Commits stratégiques ou techniques        |
| 🔄    | Mise à jour                    | Commit de refacto ou d’update             |
| 📝    | Journal / historique           | Liste des derniers commits                |
| 🧬    | Changement dans l’arborescence | Commit impactant la structure du code     |
| 🗂️   | Fichiers                       | Plusieurs commits sur différents fichiers |
