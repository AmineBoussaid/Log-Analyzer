from dal import AccessLogDao

def get_stats_par_mois():
    stats = AccessLogDao.getStatsParMois()
    return [
        {'date': stat[0], 'hits': stat[1], 'unique_visitors': stat[2]}
        for stat in stats
    ]

def get_uri_stats():
    stats = AccessLogDao.getUriStats()
    return [
        {'uri': stat[0], 'hits': stat[1], 'unique_visitors': stat[2]}
        for stat in stats
    ]

def get_browser_stats():
    stats = AccessLogDao.getBrowserStats()
    return [
        {'browser': stat[0], 'hits': stat[1], 'unique_visitors': stat[2]}
        for stat in stats
    ]

def get_not_found_urls():
    not_found_urls = AccessLogDao.getNotFoundUrls()
    return [
        {'uri': url[0], 'not_found_count': url[1]}
        for url in not_found_urls
    ]


def get_operating_systems():
    stats = AccessLogDao.getOperatingSystems()
    return [
        {'operating_system': stat[0], 'hits': stat[1], 'unique_visitors': stat[2]}
        for stat in stats
    ]

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