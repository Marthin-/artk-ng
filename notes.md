# notes de développement (entre autres)

### versions de python

kivy utilise un truc maison pour twisted qui n'existe pas en python3. On reste sur kivy et on adapte, ou bien on passe à un autre GUI ?
A mon avis python3 est à privilégier, ne serait-ce que pour la gestion des accents (*no comment...*)

En farfouillant du côté de Twisted on trouve deux GUI "pratiques" (i.e. multiplateforme) qui sont intégrés : GTK+ ou simplement pytk. Privilégier pytk ? (installé de base)