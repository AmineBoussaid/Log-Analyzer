async function fetchAuthFailuresByIp() {

        const response = await fetch('/api/auth-failures-by-ip');
        const data = await response.json();
        return data;
}

function createAuthFailuresByIpChart(data) {

    const labels = data.map(item => item.ip);
    const authFailures = data.map(item => item.auth_failures);

    const ctx = document.getElementById('authFailuresByIpChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Auth Failures',
                    data: authFailures,
                    backgroundColor: 'rgb(0, 84, 153)',
                    borderColor: 'rgb(0, 84, 153,1)',
                    borderWidth: 1,
                    yAxisID: 'y'
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 25000,
                    title: {
                        display: true,
                        text: 'Count'
                    }
                }
            }
        }
    });
}


/*******************************************/

function fetchAuthFailuresByPeriod() {
    return fetch('/api/auth-failures-by-period')
        .then(response => response.json())
        .then(data => {
            return data.map(item => ({
                day: new Date(item.day).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric'
                }),
                auth_failures: item.auth_failures
            }));
        });
}

function createAuthFailuresByPeriodChart(data) {
    const labels = data.map(item => item.day);
    const authFailures = data.map(item => item.auth_failures);

    const ctx = document.getElementById('authFailuresByPeriodChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Auth Failures',
                data: authFailures,
                backgroundColor: 'rgba(255, 0, 0, 0.6)',
                borderColor: 'rgba(255, 0, 0, 1)',
                borderWidth: 1,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Count'
                    }
                }
            }
        }
    });
}




/*********************************************************/

async function main() {

    const authFailuresByIp = await fetchAuthFailuresByIp();
    createAuthFailuresByIpChart(authFailuresByIp);

    const authFailuresByPeriod = await fetchAuthFailuresByPeriod();
    createAuthFailuresByPeriodChart(authFailuresByPeriod);

}

main();
