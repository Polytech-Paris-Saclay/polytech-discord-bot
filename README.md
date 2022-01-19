# tesla-internship-and-oasis-grades-scrapper
Petit bot Discord pour avertir de :
- nouvelles offres de stage sur le site de Tesla
- nouvelles notes sur Oasis (Polytech Paris-Saclay)

---

### Installer les dépendances
`pip install -r requirements.txt`

---

Les fichiers `oasis.py` et `tesla.py` définissent respectivement les fonctions :
- `getGrades()`
- `getInternships()`, `getInternshipInfos()`

et sont indépendants (ils peuvent être appelés seuls sans passer par `main.py`)

---

Les identifiants oasis et/ou le token Discord doivent être placés dans un fichier `.env` sous la forme
```
# Oasis (Polytech Paris-Saclay)
LOGIN = 01234567 #Numéro étudiant
PASSWORD = MotDePasse

# Discord bot
TOKEN = token-bot-discord
```

[Comment créer un bot Discord ?](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)

---

### *Alexandre MALFREYT*
