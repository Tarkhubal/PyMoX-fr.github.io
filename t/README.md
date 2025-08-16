# Doc divers - Mémo - ToDo

## reset projet GH

```bash

// Reset main / commit XXX (En gardant les fichiers)
(Save locale des fichier sans .git et sans .venv)

Effacer tous les tags et releases plus souhaités

git checkout -b temp_backup

# Trouver le hash du commit correspondant au tag exemple v1.0.1
git log --oneline --decorate | findstr "v1.0.1"

# Revenir à main
git checkout main

# Réinitialiser main au commit v1.0.1 (remplacez abcd123 par le hash réel)
git reset --hard abcd123

# Rec fichier

* Commit




// Reset / Écrase main actuelle

rm -rf .git
git init
git add .
git commit -m "Re ini"

git remote add origin https://github.com/PyMoX-fr/PyMoX-fr.github.io.git

git branch -M main  # ou master, selon convention

git push -f origin main

Créée une br sur un sha (et checkout)
git switch -c feature-old 3a5b9c2

enregistre fct pour del br local & distante
git config --global alias.delbr '!f() { git branch -D "$1" && git push origin --delete "$1"; }; f'

git delbr uuu
```
