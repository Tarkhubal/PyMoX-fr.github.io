[Retour Sommaire](index.md)
<!-- 
# lines.append("""/// details | 🚧 Unreleased Commits
# type: warning
# attrs: {class: "unreleased-commits", id: "unreleased", data-status: "pending"}
# open: true

# - feat: add dark mode toggle
# - fix: resolve crash on startup
# - chore: update dependencies
# ///""")

lines.append('/// details | 🚧 Unreleased Commits\n    type: warning\n    attrs: {class: "unreleased-commits", id: "unreleased", data-status: "pending"}\n    open: true\n    \n    - feat: add dark mode toggle\n    - fix: resolve crash on startup\n    - chore: update dependencies\n///')

lines.append("""/// details | In titre Ok ici\n    type: warning\n    attrs: {}\n    open: true\n    \n```js
              
  Content\n* feat: add dark mode toggle\n* fix: resolve crash on startup\n* chore: update dependencies\n///""")

# lines.append('/// details | In titre Ok 2 ici\n    type: warning\n    attrs: {}\n    open: true\n    \n```## Content\n* feat: add dark mode toggle\n* fix: resolve crash on startup\n* chore: update dependencies\n///```')

lines.append('\n---\n')

lines.append('<details class="optional-class"><summary>Text</summary><p>Content</p></details>')

lines.append('??? details-note "<span style="color:red">ATTENTION : **Page en travaux**</span> :-)"\n    Réfection du style si des commits de type Unreleased existent')
  -->
??? warning "Default WARNING"
    Content

??? unreleased-block "📦 Unreleased-block (???)"
    Liste des commits...

/// details | 🍵 Unreleased-block (///)
    type: unreleased-block
    open: false
    attrs: {class: 'unreleased-block'}
Content 2
///

<hr>

* [ ] Recherche pour ajouter fonction cliquer pour 'Copier' (Dans le clipboard)

* [ ] → Déplacer le title sur le centre du texte ?

<div class="copy-target" data-copy title="">
  Exemple de texte que l'on veut pouvoir cliquer pour être copié dans le presse-papier.
</div>
