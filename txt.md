Dans mon VSC, j'ai une extension qui gère les TODO, je lui ai défini 8 TAGS (Chacun a sa couleur).


Dès que c'est dans un fichier, quelqu'il soit (md, py, txt, js, json, yml, yoml, etc...), l'extension identifie ce tag.
Nous avons ainsi 8 tags distincts :

2fix à solutioner
2dbug oki2
2ar à enlever
2see à voir

* [/] en cours
* [ ] à faire
2do à faire
2let à laisser

Je voudrais un script py qui parcours mon projet (en ignorant /site, .venv, etc...) et me dresse la liste des tags (et du texte qui suit), puis après une ligne de séparation, le total par tag (l'idéal serait sous forme d'un tableau).

Pour info, mon projet actuel contient parmis ses fichiers: 2fix: 4 , 1 dbug, 1 2ar, 1 2see, 1 * [/], 2 * [ ], 1 2do et 1 2let.

Note : j'ai commencé ce script ici: t/scan_todos.py
