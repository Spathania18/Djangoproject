document.addEventListener('DOMContentLoaded', function () {
    // Chart Contexts
    const jobTypeCtx = document.getElementById('jobTypeChart').getContext('2d');
    const companyCtx = document.getElementById('companyChart').getContext('2d');
    const dateCtx = document.getElementById('dateChart').getContext('2d');

    // Initialize Charts
    let jobTypeChart, companyChart, dateChart;

    function initializeCharts(data) {
        // Initialize Job Type Chart
        jobTypeChart = new Chart(jobTypeCtx, {
            type: 'pie',
            data: {
                labels: data.jobTypes || [],
                datasets: [{
                    label: 'Job Type Distribution',
                    data: data.jobTypeData || [],
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                }]
            }
        });

        // Initialize Company Chart
        companyChart = new Chart(companyCtx, {
            type: 'bar',
            data: {
                labels: data.companyNames || [],
                datasets: [{
                    label: 'Applications by Company',
                    data: data.companyCounts || [],
                    backgroundColor: '#36A2EB',
                }]
            },
            options: {
                scales: {
                    x: { beginAtZero: true },
                    y: { beginAtZero: true }
                }
            }
        });

        // Initialize Date Chart if data is available
        if (data.insightyearLabels && data.insightyearCounts) {
            dateChart = new Chart(dateCtx, {
                type: 'line',
                data: {
                    labels: data.insightyearLabels || [],
                    datasets: [{
                        label: 'Applications by Date',
                        data: data.insightyearCounts || [],
                        borderColor: '#FF6384',
                        fill: false,
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time', // Time scale
                            time: {
                                unit: 'day' // Display unit
                            }
                        },
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } else {
            console.warn("No data available for the Applications by Date chart.");
        }
    }

    function fetchDashboardData() {
        // Replace 'your-username' with the actual username or get it dynamically
        fetch('/api/dashboard/?username=sumit')
            .then(response => response.json())
            .then(data => {
                console.log('Fetched Dashboard Data:', data);
                initializeCharts(data);
            })
            .catch(error => console.error('Error fetching dashboard data:', error));
    }

    fetchDashboardData();
});
