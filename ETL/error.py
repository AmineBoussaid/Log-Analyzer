import sys
sys.path.append(r"")

from models import ErrorLog

import re
import datetime
import mysql.connector

def extract_from_error_log(log_file_path: str):
    """
    Fonction pour extraire les données à partir d'un fichier de logs d'erreurs.
    """
    error_logs = []
    with open(log_file_path, 'r') as file:
        for line in file:
            match = re.match(r'\[(.*?)\] \[(.*?)\] \[pid (.*?)\] (.*)', line)
            if match:
                timestamp_str, module_and_severity, pid, message = match.groups()
                # Séparation du module et du niveau de gravité
                module, severity = module_and_severity.split(':')
                # Conversion de la chaîne de date en objet datetime
                timestamp = datetime.datetime.strptime(timestamp_str, '%a %b %d %H:%M:%S.%f %Y')
                error_log = ErrorLog(timestamp=timestamp, severity=severity, pid=int(pid), module=module, message=message)
                error_logs.append(error_log)
    return error_logs


def load_to_database(error_logs,db_connection):
    """
    Fonction pour charger les données dans la base de données.
    """
    try:

        cursor = db_connection.cursor()

        for error_log in error_logs:
            cursor.execute("INSERT INTO error_log (timestamp, severity, module, pid, message) VALUES (%s, %s, %s, %s, %s)", 
                            (error_log.timestamp, error_log.severity, error_log.module, error_log.pid, error_log.message))

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
    # Chemin vers le fichier de logs d'erreurs
    error_log_file_path = (r"Logs\error_log")
    
    # Extraction des données du fichier de logs d'erreurs
    error_logs = extract_from_error_log(error_log_file_path)

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
    load_to_database(error_logs, db_connection)
