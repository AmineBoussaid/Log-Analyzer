from collections import defaultdict
from typing import List

import requests
from dal import AccessLogDao, SecureAuthDao, UserDao
from models import User



class UserService:
    users:List[User] = UserDao.getAllUsers()
    
    @staticmethod
    def getAllUsers():
        return UserService.users
    
    @staticmethod
    def login(email,passwors)->User:
        for u in UserService.users:
            if u.email == email and u.password == passwors:
                return u
        return None
    
    @staticmethod
    def register(email,password):
        UserDao.register(User(email,password))


class AccessService:
    @staticmethod 
    def get_stats_par_mois():
        stats = AccessLogDao.getStatsParMois()
        return [
            {'date': stat[0], 'hits': stat[1], 'unique_visitors': stat[2]}
            for stat in stats
        ]
    
    @staticmethod 
    def get_uri_stats():
        stats = AccessLogDao.getUriStats()
        return [
            {'uri': stat[0], 'hits': stat[1], 'unique_visitors': stat[2]}
            for stat in stats
        ]
    
    @staticmethod
    def get_browser_stats():
        stats = AccessLogDao.getBrowserStats()
        return [
            {'browser': stat[0], 'hits': stat[1], 'unique_visitors': stat[2]}
            for stat in stats
        ]
    
    @staticmethod
    def get_not_found_urls():
        not_found_urls = AccessLogDao.getNotFoundUrls()
        return [
            {'uri': url[0], 'not_found_count': url[1]}
            for url in not_found_urls
        ]

    @staticmethod
    def get_operating_systems():
        stats = AccessLogDao.getOperatingSystems()
        return [
            {'operating_system': stat[0], 'hits': stat[1], 'unique_visitors': stat[2]}
            for stat in stats
        ]
    
    @staticmethod
    def get_overview_stats():
        stats = AccessLogDao.getOverviewStats()
        if stats:
            return {
                'total_requests': stats[0],
                'valid_requests': stats[1],
                'failed_requests': stats[2],
                'unique_visitors': stats[3],
                'referrers': stats[4],
                'not_found': stats[5],
                'requested_files': stats[6],
                'tx_amount': stats[7]
            }
        else:
            return {}
        


    @staticmethod
    def getFileTypeStats():
        stats = AccessLogDao.getFileTypeStats()
        return [
            {'file_type': stat[0], 'visitors': stat[1], 'hits': stat[2]}
            for stat in stats
        ]
    


    @staticmethod
    def get_ip_stats():
        stats = AccessLogDao.getIpStats()
        return [
            {'ip': stat[0], 'visitors': stat[1], 'hits': stat[2]}
            for stat in stats
        ]
    

    @staticmethod
    def get_response_code_stats():
        stats = AccessLogDao.getResponseCodeStats()
        return [
            {'code_category': stat[0], 'visitors': stat[1], 'hits': stat[2]}
            for stat in stats
        ]
    

    @staticmethod
    def get_geo_location(ip):
        api_token = '1c1ac043ce78d8'
        url = f'https://ipinfo.io/{ip}?token={api_token}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                'ip': ip,
                'country': data.get('country', 'Unknown'),
                'city': data.get('city', 'Unknown'),
            }
        else:
            return {
                'ip': ip,
                'country': 'Unknown',
                'city': 'Unknown',
            }

    @staticmethod
    
    def get_geo_locations():
        access_data = AccessLogDao.get_all_access_with_ip()[:50]
        geo_data = defaultdict(lambda: {'hits': 0, 'unique_visitors': set()})
        
        for ip, hits, unique_visitors in access_data:
            # Utiliser l'adresse IP pour obtenir le pays
            country = AccessService.get_geo_location(ip)['country']
            
            # Ajouter les hits et les visiteurs uniques au pays correspondant
            geo_data[country]['hits'] += hits
            geo_data[country]['unique_visitors'].add(ip)
        
        result = []
        for country, data in geo_data.items():
            result.append({
                'country': country,
                'hits': data['hits'],
                'unique_visitors': len(data['unique_visitors'])
            })
        
        return result




class SecureAuthService:
    @staticmethod
    def get_auth_failures_by_ip():
        stats = SecureAuthDao.getAuthfailuresIp()
        return [
            {'ip': stat[0], 'auth_failures': stat[1]}
            for stat in stats
        ]
    


    @staticmethod
    def get_auth_failures_by_period():
        stats = SecureAuthDao.get_auth_failures_by_period()
        return [
            {'day': stat[0], 'auth_failures': stat[1]}
            for stat in stats
        ]


    


