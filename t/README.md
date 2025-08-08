# Doc divers

## reset projet GH

rm -rf .git

git init
git add .
git commit -m "Re ini"

git remote add origin https://github.com/ton-utilisateur/ton-depot.git

git branch -M main  # ou master, selon ta convention
git push -f origin main
