import sys
sys.path.append(r"")

from models import AccessLog

import re
import datetime
import mysql.connector

def extract_from_log_file(log_file_path):
    """
    Fonction pour extraire les données à partir d'un fichier de logs.
    """
    access_logs = []
    with open(log_file_path, 'r') as file:
        for line in file:
            # Utilisation d'expressions régulières pour extraire les champs
            match = re.match(r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S*)" (\d{3}) (\d+) "([^"]*)" "([^"]*)"', line)
            if match:
                ip, _, _, timestamp_str, http_method, uri, http_protocol, response_code, response_size, referer, user_agent = match.groups()
                timestamp = datetime.datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z')
                access_log = AccessLog(ip=ip, timestamp=timestamp, http_method=http_method, uri=uri, http_protocol=http_protocol, response_code=int(response_code), response_size=int(response_size), referer=referer, user_agent=user_agent)
                access_logs.append(access_log)
    return access_logs

def load_to_database(access_logs, db_connection):
    """
    Fonction pour charger les données dans la base de données.
    """
    try:
        cursor = db_connection.cursor()

        for access_log in access_logs:
            # Insertion des données dans la table de la base de données
            cursor.execute("INSERT INTO access_log (ip, timestamp, http_method, uri, http_protocol, response_code, response_size, referer, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                            (access_log.ip, access_log.timestamp, access_log.http_method, access_log.uri, access_log.http_protocol, access_log.response_code, access_log.response_size, access_log.referer, access_log.user_agent))

        db_connection.commit()
        print("Les données ont été chargées avec succès dans la base de données.")

    except mysql.connector.Error as error:
        print(f"Erreur lors du chargement des données dans la base de données: {error}")

    finally:
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("Connexion à la base de données fermée.")

# Exemple d'utilisation des fonctions

if __name__ == "__main__":
    # Chemin vers le fichier de logs
    log_file_path = (r"Logs\access_log")

    # Extraction des données du fichier de logs
    access_logs = extract_from_log_file(log_file_path)

    # Connexion à la base de données MySQL
    db_connection = mysql.connector.connect(
        user='root',
        passwd='',
        host='localhost',
        port=3306,
        database="logsbd",
        charset='utf8'
    )

    # Chargement des données dans la base de données
    load_to_database(access_logs, db_connection)
