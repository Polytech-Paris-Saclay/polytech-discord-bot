# tesla-internship-and-oasis-grades-scrapper
Petit bot Discord pour avertir de :
- nouvelles offres de stage sur le site de Tesla
- nouvelles notes sur Oasis

---

Les fichiers `oasis.py` et `tesla.py` définissent respectivement les fonctions :
- `getGrades()`
- `getInternships()`, `getInternshipInfos()`

et sont indépendants (ils peuvent être appelés seuls sans passer par `main.py`)

---

Les identifiants oasis et/ou le token Discord doivent être placés dans un fichier `.env` sous la forme
```
# Oasis
LOGIN = 01234567
PASSWORD = MotDePasse

# Discord bot
TOKEN = token-bot-discord
```

---

### *Alexandre MALFREYT*
