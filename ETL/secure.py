import sys
sys.path.append(r"C:\Users\ADMIN\Desktop\cs\3eme annee\Python\Projet Python")

import re
import datetime
import mysql.connector


def extract_secure(file):
    entries = []
    auth = []
    format_string = "%b %d %H:%M:%S"
    
    regex0 = r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\w+)\s+sshd\[(\d+)\]:\s+(.+)\s+for\s+(\w+)\s+from\s+(\d+\.\d+\.\d+\.\d+)\s+port\s+(\d+).*\s+.*(ssh2|preauth).*'
    regex1 = r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\w+)\s+sshd\[(\d+)\]:\s+(.+)\s+\w+\s+(\d+\.\d+\.\d+\.\d+)\s+port\s+(\d+).*\s+.*(ssh2|preauth).*'
    regex2 = r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\w+)\s+sshd\[(\d+)\]:?\s?.*:\s+(.+);\s+logname=+(.*)\s+uid=+(.*)\s+euid=?(.*)\s+tty=+(.*)\s+ruser=(.*)\s+rhost=(.*)\s{2,}user=(.*)'
    regex4 = r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\w+)\s+sshd\[(\d+)\]:?\s?.*:\s+(.+);\s+logname=+(.*)\s+uid=+(.*)\s+euid=?(.*)\s+tty=+(.*)\s+ruser=(.*)\s+rhost=(.*)'
    regex3 = r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\w+)\s+sshd\[(\d+)\]:?\s?.*:\s?(.+);\s+user\s+(.*)'

    with open(file, 'r') as f:
                for line in f:
                    match0 = re.match(regex0, line)
                    match1 = re.match(regex1, line)
                    match2 = re.match(regex2, line)
                    match3 = re.match(regex3, line)
                    match4 = re.match(regex4, line)

                    if match0:
                        date,hote,sshd,meg,user,ip,port,ssh = match0.groups()
                        
                        entries.append((datetime.datetime.strptime(date,format_string),hote,sshd,meg,user,ip,int(port),ssh))
                    elif match1:
                        date,hote,sshd,meg,ip,port,ssh = match1.groups()
                        
                        entries.append((datetime.datetime.strptime(date,format_string),hote,sshd,meg,'',ip,int(port),ssh))
                    elif match2:
                        
                        date,hote,sshd,meg,logname,uid,euid,tty,ruser,rhost,user = match2.groups()
                        
                        auth.append((datetime.datetime.strptime(date,format_string),hote,sshd,meg,logname,int(uid),int(euid),tty,ruser,rhost,user))
                    elif match4:
                        
                        date,hote,sshd,meg,logname,uid,euid,tty,ruser,rhost = match4.groups()
                        
                        auth.append((datetime.datetime.strptime(date,format_string),hote,sshd,meg,logname,int(uid),int(euid),tty,ruser,rhost,''))
                    elif match3:
                        
                        date,hote,sshd,meg,user = match3.groups()
                        
                        auth.append((datetime.datetime.strptime(date,format_string),hote,sshd,meg,'',None,None,'','','',user))
    return entries,auth

def load_secure(List) :
        try:
            cursor = db_connection.cursor()
            for elem in List :
                cursor.execute("INSERT INTO secure_Log (date,hote,sshd,meg,user,ip,port,ssh) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                               (elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7]))
            
            db_connection.commit()
            print("Les données ont été chargées avec succès dans la base de données.")

        except mysql.connector.Error as error:
            print(f"Erreur lors du chargement des données dans la base de données: {error}")

        #finally:
         #   if db_connection.is_connected():
          #      cursor.close()
          #      db_connection.close()
           #     print("Connexion à la base de données fermée.")


def load_secure_auth(List) :
        try:
            
            cursor = db_connection.cursor()
            for elem in List :
                cursor.execute("INSERT INTO secure_auth (date,hote,sshd,meg,logname,uid,euid,tty,ruser,rhost,user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                               (elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7], elem[8], elem[9], elem[10]))
            
            db_connection.commit()
            print("Les données ont été chargées avec succès dans la base de données.")

        except mysql.connector.Error as error:
            print(f"Erreur lors du chargement des données dans la base de données: {error}")

        finally:
            if db_connection.is_connected():
                cursor.close()
                db_connection.close()
                print("Connexion à la base de données fermée.")


if __name__ ==  "__main__":

    secure_file_path = (r"C:\Users\ADMIN\Desktop\cs\3eme annee\Python\Projet Python\Logs\secure_log")

    secure,auth = extract_secure(secure_file_path)

    # Connexion à la base de données MySQL
    db_connection = mysql.connector.connect(
        user='root',
        passwd='',
        host='localhost',
        port=3306,
        database="logsbd",
        charset='utf8'
    )

    load_secure(secure)
    load_secure_auth(auth)  

      