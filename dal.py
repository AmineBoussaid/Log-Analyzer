import mysql.connector
from mysql.connector import Error

from models import User

class DataBase:
    SERVER_NAME = 'localhost'
    DATABASE_NAME = 'logsbd'
    USER = 'root'
    PASSWORD = ''
    Connection = None

    @staticmethod
    def getConnection():
        try:
            if DataBase.Connection is None or not DataBase.Connection.is_connected():
                conn = mysql.connector.connect(
                    host=DataBase.SERVER_NAME,
                    database=DataBase.DATABASE_NAME,
                    user=DataBase.USER,
                    password=DataBase.PASSWORD,
                    charset='utf8'
                )
                DataBase.Connection = conn
        except Error as e:
            print(f"Error: {e}")
        return DataBase.Connection
    

class UserDao:
    @staticmethod
    def getAllUsers() -> list[User]:
        try:
            conn=DataBase.getConnection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user")
            user_data = cursor.fetchall()

            conn.commit()
            cursor.close()
            conn.close()


            users = [User(*data) for data in user_data] if user_data else []
            return users
        except Exception as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def register(user: User) -> str:
        try:
            conn=DataBase.getConnection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO user (Email, Pasword) VALUES (%s, %s)",
            (user.email, user.password))

            conn.commit()
            cursor.close()
            conn.close()

            return "Registration successful."
        except Error as e:
            print(f"Error: {e}")
            return f"Registration failed. Error: {str(e)}"

class AccessLogDao:
    @staticmethod
    def getStatsParMois():
        try:
            conn = DataBase.getConnection()
            if conn is None:
                raise Error("Unable to connect to the database.")
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DATE_FORMAT(timestamp, '%Y-%m') AS month, COUNT(*) AS hits, COUNT(DISTINCT ip) AS unique_visitors
                FROM access_log
                GROUP BY month
            """)
            statsParMois = cursor.fetchall()
            conn.close()
            return statsParMois
        except Error as e:
            print(f"Erreur: {e}")
            return []
        
    @staticmethod
    def getUriStats():
        try:
            conn = DataBase.getConnection()
            cursor = conn.cursor()

            query = """
            SELECT 
                uri,
                COUNT(*) AS hits,
                COUNT(DISTINCT ip) AS unique_visitors
            FROM 
                access_log
            WHERE 
                http_method = 'GET'
            GROUP BY 
                uri
            HAVING 
                hits > 300 AND unique_visitors > 300
            ORDER BY
                hits DESC, unique_visitors DESC;
            """
            cursor.execute(query)
            uri_stats = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()

            return uri_stats
        except Error as e:
            print(f"Erreur: {e}")
            return None
        
    @staticmethod
    def getBrowserStats():
        try:
            conn = DataBase.getConnection()
            cursor = conn.cursor()

            query = """
            SELECT 
                browser,
                COUNT(*) AS hits,
                COUNT(DISTINCT ip) AS unique_visitors
            FROM (
                SELECT
                    CASE
                        WHEN user_agent LIKE '%Chrome%' AND user_agent NOT LIKE '%Chromium%' THEN 'Chrome'
                        WHEN user_agent LIKE '%Firefox%' THEN 'Firefox'
                        WHEN user_agent LIKE '%Safari%' AND user_agent NOT LIKE '%Chrome%' THEN 'Safari'
                        WHEN user_agent LIKE '%MSIE%' OR user_agent LIKE '%Trident%' THEN 'Internet Explorer'
                        WHEN user_agent LIKE '%Edge%' THEN 'Edge'
                        WHEN user_agent LIKE '%Opera%' OR user_agent LIKE '%OPR%' THEN 'Opera'
                        ELSE 'Other'
                    END AS browser,
                    ip
                FROM 
                    access_log
                WHERE 
                    http_method = 'GET'
            ) AS browser_data
            GROUP BY 
                browser
            ORDER BY 
                hits DESC;
            """
            cursor.execute(query)
            browser_stats = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()

            return browser_stats
        except Error as e:
            print(f"Erreur: {e}")
            return None
        
    @staticmethod
    def getNotFoundUrls():
        try:
            conn = DataBase.getConnection()
            cursor = conn.cursor()

            query = """
            SELECT uri, COUNT(*) AS not_found_count
            FROM access_log
            WHERE response_code = 404
            GROUP BY uri
            HAVING not_found_count >= 500
            ORDER BY not_found_count DESC;
            """
            cursor.execute(query)
            not_found_urls = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()

            return not_found_urls
        except Error as e:
            print(f"Erreur: {e}")
            return None
        

    @staticmethod
    def getOperatingSystems():
        try:
            conn = DataBase.getConnection()
            cursor = conn.cursor()

            query = """
            SELECT
                CASE
                    WHEN user_agent LIKE '%Windows%' THEN 'Windows'
                    WHEN user_agent LIKE '%Mac OS X%' THEN 'Mac OS X'
                    WHEN user_agent LIKE '%Linux%' THEN 'Linux'
                    WHEN user_agent LIKE '%Android%' THEN 'Android'
                    WHEN user_agent LIKE '%iOS%' THEN 'iOS'
                    ELSE 'Other'
                END AS operating_system,
                COUNT(*) AS hits,
                COUNT(DISTINCT ip) AS unique_visitors
            FROM
                access_log
            GROUP BY
                operating_system
            ORDER BY
                hits DESC;
            """
            cursor.execute(query)
            operatingSystems = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            return operatingSystems
        except Error as e:
            print(f"Erreur: {e}")
            return None
        

    @staticmethod
    def getOverviewStats():
        try:
            conn = DataBase.getConnection()
            cursor = conn.cursor()

            query = """
            SELECT 
                (SELECT COUNT(*) FROM access_log) AS total_requests,
                (SELECT COUNT(*) FROM access_log WHERE response_code = 200) AS valid_requests,
                (SELECT COUNT(*) FROM access_log WHERE response_code >= 400 AND response_code < 600) AS failed_requests,
                (SELECT COUNT(DISTINCT ip) FROM access_log) AS unique_visitors,
                (SELECT COUNT(DISTINCT referer) FROM access_log WHERE referer != '') AS referers,
                (SELECT COUNT(*) FROM access_log WHERE response_code = 404) AS not_found,
                (SELECT COUNT(DISTINCT uri) FROM access_log WHERE uri != '' AND uri IS NOT NULL) AS requested_files,
                (SELECT SUM(response_size) FROM access_log) AS tx_amount
            """
            cursor.execute(query)
            stats = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()

            return stats
        except Error as e:
            print(f"Erreur: {e}")
            return None
        


    @staticmethod
    def getFileTypeStats():
        try:
            conn = DataBase.getConnection()
            cursor = conn.cursor()

            query = """
            SELECT
                file_type,
                COUNT(DISTINCT ip) AS visitors,
                COUNT(*) AS hits
            FROM (
                SELECT
                    CASE
                        WHEN uri LIKE '%.jpg' THEN 'jpg'
                        WHEN uri LIKE '%.jpeg' THEN 'jpeg'
                        WHEN uri LIKE '%.png' THEN 'png'
                        WHEN uri LIKE '%.gif' THEN 'gif'
                        WHEN uri LIKE '%.css' THEN 'css'
                        WHEN uri LIKE '%.js' THEN 'js'
                        WHEN uri LIKE '%.ico' THEN 'ico'
                        WHEN uri LIKE '%.svg' THEN 'svg'
                        WHEN uri LIKE '%.woff' THEN 'woff'
                        WHEN uri LIKE '%.woff2' THEN 'woff2'
                        WHEN uri LIKE '%.ttf' THEN 'ttf'
                        WHEN uri LIKE '%.php' THEN 'php'
                        WHEN uri LIKE '%.html' THEN 'html'
                        WHEN uri LIKE '%.txt' THEN 'txt'
                        ELSE 'other'
                    END AS file_type,
                    ip
                FROM access_log
            ) AS subquery
            GROUP BY file_type
            ORDER BY hits DESC;
            """
            cursor.execute(query)
            file_type_stats = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()

            return file_type_stats
        except Error as e:
            print(f"Error: {e}")
            return None
        


    @staticmethod
    def getIpStats():
        try:
            conn = DataBase.getConnection()
            cursor = conn.cursor()

            query = """
            SELECT 
                ip,
                COUNT(DISTINCT ip) AS visitors,
                COUNT(*) AS hits
            FROM 
                access_log
            GROUP BY 
                ip
            HAVING 
                hits > 1800
            ORDER BY 
                hits DESC;
            """
            cursor.execute(query)
            ip_stats = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()

            return ip_stats
        except Error as e:
            print(f"Error: {e}")
            return None  

    
    @staticmethod
    def getResponseCodeStats():
        try:
            conn = DataBase.getConnection()
            cursor = conn.cursor()

            query = """
            SELECT
                CASE
                    WHEN response_code BETWEEN 100 AND 199 THEN '1xx (Informations)'
                    WHEN response_code BETWEEN 200 AND 299 THEN '2xx (Success)'
                    WHEN response_code BETWEEN 300 AND 399 THEN '3xx (Redirection)'
                    WHEN response_code BETWEEN 400 AND 499 THEN '4xx (Client Errors)'
                    ELSE 'Other'
                END AS code_category,
                COUNT(DISTINCT ip) AS visitors,
                COUNT(*) AS hits
            FROM access_log
            GROUP BY code_category;
            """
            cursor.execute(query)
            response_code_stats = cursor.fetchall()
            conn.close()

            return response_code_stats
        except Error as e:
            print(f"Error: {e}")
            return None




class SecureAuthDao:
    @staticmethod
    def getAuthfailuresIp():
        try:
            conn = DataBase.getConnection()
            cursor = conn.cursor()
            
            query = """
            SELECT rhost AS ip, COUNT(*) AS auth_failures
            FROM secure_auth
            WHERE meg LIKE '%authentication failure%'
            GROUP BY rhost
            HAVING
                auth_failures > 400
            ORDER BY auth_failures DESC;
            """
            
            cursor.execute(query)
            
            result = cursor.fetchall()
            conn.close()
            return result
        except Error as e:
            print(f"Error: {e}")
            return None
        

        
    @staticmethod
    def get_auth_failures_by_period():
        try:
            conn = DataBase.getConnection()
            cursor = conn.cursor()
            
            query = """
            SELECT DATE(date) AS day, COUNT(*) AS auth_failures
            FROM secure_auth
            WHERE meg LIKE '%authentication failure%'
            GROUP BY day
            ORDER BY day;
            """
            
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return result
        except Error as e:
            print(f"Error: {e}")
            return None

        
        

    
