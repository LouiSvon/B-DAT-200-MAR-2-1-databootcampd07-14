# Data Bootcamp D07 - Nobel JSON vers SQLite

## Description

Ce depot contient des exercices de transformation de donnees Nobel depuis un fichier JSON vers une base SQLite.

## Objectif

L'objectif est de lire un dataset JSON, extraire des informations utiles et construire progressivement une base relationnelle.

## Stack / technologies

- Python
- JSON
- SQLite
- `sqlite3`

## Fonctionnalites principales

- Lecture d'un fichier JSON.
- Extraction d'informations sur les laureats Nobel.
- Creation d'un schema SQLite avec tables `country`, `category`, `laureate` et `prize`.
- Insertion des categories.
- Insertion des pays.
- Insertion des laureats avec normalisation simple des dates.

## Structure

```text
.
├── nobels.json
├── task00.py
├── task01.py
├── task02.py
├── task03.py
├── task04.py
└── task05.py
```

## Lancement

Exemple d'utilisation depuis Python :

```python
from task02 import create_database
from task03 import insert_categories
from task04 import insert_countries
from task05 import insert_laureates

create_database("nobels.db")
insert_categories("nobels.json", "nobels.db")
insert_countries("nobels.json", "nobels.db")
insert_laureates("nobels.json", "nobels.db")
```

## Remarques

Les scripts ne fournissent pas de pipeline complet en ligne de commande. Ils sont organises sous forme de fonctions d'exercices.
