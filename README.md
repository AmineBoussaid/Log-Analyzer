# Log-Analyzer

Log-Analyzer est un outil de surveillance et d'analyse des journaux d'accès web. Il permet d'extraire, de transformer et de charger les données des journaux d'accès dans une base de données, puis de visualiser des statistiques et des tendances à travers une interface web conviviale.

## Fonctionnalités

- **Extraction des logs** : Extraction des données des journaux d'accès et d'erreurs.
- **Chargement des données** : Stockage des données extraites dans une base de données MySQL.
- **Analyse des données** : Calcul des statistiques telles que les visiteurs uniques, les hits, les fichiers demandés, etc.
- **Visualisation des données** : Affichage des statistiques sous forme de graphiques et de tableaux sur une interface web.

## Prérequis

- Python 3.6 ou supérieur
- MySQL
- Flask
- Modules Python : `mysql-connector-python`, `flask`


## Organisation des fichiers

- **models.py** : Définition des classes de modèles pour les données de logs.
- **app.py** : Fichier principal de l'application Flask.
- **etl.py** : Script d'extraction, de transformation et de chargement des données.
- **dal.py** : Couche d'accès aux données pour interagir avec la base de données.
- **templates/** : Dossier contenant les templates HTML.
- **static/js/** : Dossier contenant les fichiers JavaScript pour les visualisations.
- **static/css/** : Dossier contenant les fichiers CSS pour le style.



## Utilisation
1. Lancer le script d'extraction et de chargement des logs :
```bash
python etl.py
```

2. Démarrer le serveur Flask :
```bash
python app.py
```
