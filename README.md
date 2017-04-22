# artk-ng
### Another rpg toolkit - next generation

---

# 1. L'idée de base:

* Un ensemble d'outils pour faire du JdR à distance de façon automatisée en modèle client-serveur :
    1. Un chat qui intègre les lancers de dés / les jets spéciaux
    2. Des templates de feuilles de personnage en yaml
    3. Une interface de vue du groupe (avatars, statuts, PV...)
    4. Un éditeur de maps ASCII/svg
    5. Des déclarations de système de jeu dynamiques en yaml/json (?)
    6. Une vue MJ/joueur (infos supplémentaires, accès aux feuilles de perso...)

# 2. Le chat:

* Classique, implémente des commandes style /d20, /attaque, /cp:perception
* Le but : être générique pour pouvoir se rendre indépendant du système

> Ex:
> /cp:perception lance 1d20+perception à Pathfinder ou 1d10 + perception + empathie à Esteren

* possibilité de PM

# 3. Les templates:

## Une feuille de perso pour un système donné en yaml :

>---
>- info:
>  nom: fonzie
>  classe: barbare
>  niveau: 4
>  pv: 32
>
>- defenses:
>  ca:
>    normal: 20
>    depourvu: 16
>    contact: 12
>  ref: 5
>  vig: 5
>  vol: 3
>  ...

# 4. Library
- http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php
- http://pyyaml.org/
# 5. Déclaration de systèmes:

On pourrait faire un système qui permet de déclarer le fonctionnement d'un système de jeu en yaml, pour pouvoir utiliser les outils avec n'importe quel jeu:
-> implique d'extraire des informations générales entre les différents type de jdr attaque/défense ?
>---
>- systeme: pathfinder
>- attaque:
>  normal: 1d20+BBA+For
>  puissance: -2
>  
>- degats:
>  normal: arme+For
>  puissance: +4
>  ...
>  
>- compétences:
>  natation: force
>  escalade: force
>  premiers secours: sagesse
>  representation: charisme
>    ...

# 6. Générateur de maps en ascii/wysiwyg

Traduit de l'ascii et crée une image avec (need pack de textures): 

    ##+##
    #   #
    # T #
    #####
    
et par exemple # devient une case de mur, ^ un escalier qui monte, v un qui descend, T une table, + une porte...

    ##########
    #   vv   #
    #        #
    +   TT   #
    #        #
    #   $$   #
    ##########
