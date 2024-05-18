async function fetchOverviewStats() {
    const response = await fetch('/api/overview-stats');
    const data = await response.json();
    return data;
}

function displayOverviewStats(stats) {
    document.getElementById('totalRequests').innerText = stats.total_requests;
    document.getElementById('validRequests').innerText = stats.valid_requests;
    document.getElementById('failedRequests').innerText = stats.failed_requests;
    document.getElementById('uniqueVisitors').innerText = stats.unique_visitors;
    document.getElementById('referrers').innerText = stats.referrers;
    document.getElementById('notFound').innerText = stats.not_found;
    document.getElementById('requestedFiles').innerText = stats.requested_files;
    document.getElementById('txAmount').innerText = (stats.tx_amount / (1024 * 1024)).toFixed(2) + ' MiB';  // Convert bytes to MiB
}


async function fetchData() {
    const response = await fetch('/api/stats');
    const data = await response.json();
    return data;
}

function createChart(data) {
    const ctx = document.getElementById('visitorsChart').getContext('2d');
    const labels = data.map(item => item.date);
    const hits = data.map(item => item.hits);
    const visitors = data.map(item => item.unique_visitors);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Hits',
                    data: hits,
                    backgroundColor: 'rgb(0, 84, 153)',
                    borderColor: 'rgb(0, 84, 153,1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    label: 'Visiteurs Uniques',
                    data: visitors,
                    backgroundColor: 'rgb(202, 93, 4)',
                    borderColor: 'rgb(202, 93, 4,1)',
                    borderWidth: 1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Hits'
                    }
                },
                y1: {
                    beginAtZero: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Visiteurs Uniques'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}

/****************************************** */

async function fetchUriStats() {
    const response = await fetch('/api/uri_stats');
    const data = await response.json();
    return data;
}

function createUriChart(data) {
    const ctx = document.getElementById('uriChart').getContext('2d');
    const labels = data.map(item => item.uri.length > 15 ? item.uri.substring(0, 15) + '...' : item.uri);
    const hits = data.map(item => item.hits);
    const visitors = data.map(item => item.unique_visitors);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Hits',
                    data: hits,
                    backgroundColor: 'rgb(0, 84, 153)',
                    borderColor: 'rgb(0, 84, 153,1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    label: 'Visiteurs Uniques',
                    data: visitors,
                    backgroundColor: 'rgb(202, 93, 4)',
                    borderColor: 'rgb(202, 93, 4,1)',
                    borderWidth: 1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5000,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Hits'
                    }
                },
                y1: {
                    beginAtZero: true,
                    max: 2000,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Visiteurs Uniques'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}

/*********************************************/


async function fetchBrowserStats() {
    const response = await fetch('/api/browser_stats');
    const data = await response.json();
    return data;
}

function createBrowserChart(data) {
    const ctx = document.getElementById('browserChart').getContext('2d');
    const labels = data.map(item => item.browser);
    const hits = data.map(item => item.hits);
    const visitors = data.map(item => item.unique_visitors);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Hits',
                    data: hits,
                    backgroundColor: 'rgb(0, 84, 153)',
                    borderColor: 'rgb(0, 84, 153,1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    label: 'Visiteurs Uniques',
                    data: visitors,
                    backgroundColor: 'rgb(202, 93, 4)',
                    borderColor: 'rgb(202, 93, 4,1)',
                    borderWidth: 1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 150000,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Hits'
                    }
                },
                y1: {
                    beginAtZero: true,
                    max: 15000,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Visiteurs Uniques'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}



/********************************************* */


async function fetchNotFoundUrls() {
    const response = await fetch('/api/not_found_urls');
    const data = await response.json();
    return data;
}

function createNotFoundChart(data) {
    const ctx = document.getElementById('notFoundChart').getContext('2d');
    const labels = data.map(item => item.uri);
    const counts = data.map(item => item.not_found_count);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '404 Not Found',
                data: counts,
                backgroundColor: 'rgb(0, 84, 153)',
                borderColor: 'rgb(0, 84, 153,1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10000,
                    title: {
                        display: true,
                        text: 'Count'
                    }
                }
            }
        }
    });
}


/************************************************ */

async function fetchOperatingSystemStats() {
    const response = await fetch('/api/operating-systems');
    const data = await response.json();
    return data;
}

function createBarChart(data) {
    const labels = data.map(item => item.operating_system);
    const hits = data.map(item => item.hits);
    const uniqueVisitors = data.map(item => item.unique_visitors);

    const ctx = document.getElementById('osChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Hits',
                    data: hits,
                    backgroundColor: 'rgb(0, 84, 153)',
                    borderColor: 'rgb(0, 84, 153,1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                    
                },
                {
                    label: 'Unique Visitors',
                    data: uniqueVisitors,
                    backgroundColor: 'rgb(202, 93, 4)',
                    borderColor: 'rgb(202, 93, 4,1)',
                    borderWidth: 1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100000,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Hits'
                    }
                },
                y1: {
                    beginAtZero: true,
                    max: 15000,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Visiteurs Uniques'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}


async function main() {

    const stats = await fetchOverviewStats();
    displayOverviewStats(stats);
    
    const data = await fetchData();
    createChart(data);

    const urls = await fetchUriStats();
    createUriChart(urls);

    const browserData = await fetchBrowserStats();
    createBrowserChart(browserData);

    const notFoundData = await fetchNotFoundUrls();
    createNotFoundChart(notFoundData);

    const Systemdata = await fetchOperatingSystemStats();
    createBarChart(Systemdata);
}

main();

