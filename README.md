# Polytech Bot (Discord)
Bot Discord du serveur PEIP1 Polytech Paris-Saclay, pour avertir de :
- nouvelles offres de stage sur le site de Tesla
- nouvelles notes sur Oasis (Polytech Paris-Saclay)
- prochains bus à la fin d'une journée de cours

---

### Installer les dépendances
`pip install -r requirements.txt`

---

Les fichiers `oasis.py`, `tesla.py` et `bus.py` définissent respectivement les fonctions :
- `getGrades()`
- `getInternships()`, `getInternshipInfos()`
- `getNextBusses()`

et sont indépendants (ils peuvent être appelés seuls sans passer par `main.py`)

---

Les identifiants oasis et/ou le token Discord doivent être placés dans un fichier `.env` sous la forme
```
# Oasis (Polytech Paris-Saclay)
LOGIN = 01234567 #Numéro étudiant
PASSWORD = MotDePasse

# Discord bot
TOKEN = token-bot-discord

# Agenda url (.cal)
AGENDA_URL = https://www.your-school.edu/agenda.ical
```

[Comment créer un bot Discord ?](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)

---

### *Alexandre MALFREYT*
