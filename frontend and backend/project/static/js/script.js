document.addEventListener("DOMContentLoaded", function() {
    const realtimeCtx = document.getElementById('realtime-chart').getContext('2d');
    const historyCtx = document.getElementById('history-chart').getContext('2d');

    const realtimeChart = new Chart(realtimeCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Heartbeat',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                yAxisID: 'y',
            }, {
                label: 'Pulse',
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                yAxisID: 'y1',
            }]
        },
        options: {
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    min: 50,
                    max: 150
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    min: 50,
                    max: 150,
                    grid: {
                        drawOnChartArea: false
                    },
                }
            }
        }
    });

    const historyChart = new Chart(historyCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Heartbeat',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                yAxisID: 'y',
            }, {
                label: 'Pulse',
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                yAxisID: 'y1',
            }]
        },
        options: {
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    min: 50,
                    max: 150
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    min: 50,
                    max: 150,
                    grid: {
                        drawOnChartArea: false
                    },
                }
            }
        }
    });

    function getRandomData() {
        const heartbeat = Math.floor(Math.random() * 60) + 60; // 60-120之间的随机数
        const pulse = Math.floor(Math.random() * 60) + 60;     // 60-120之间的随机数
        return { heartbeat, pulse };
    }

    function updateCharts() {
        const newData = getRandomData();
        const timestamp = new Date().toLocaleTimeString();

        if (realtimeChart.data.labels.length > 20) {
            realtimeChart.data.labels.shift();
            realtimeChart.data.datasets[0].data.shift();
            realtimeChart.data.datasets[1].data.shift();
        }

        realtimeChart.data.labels.push(timestamp);
        realtimeChart.data.datasets[0].data.push(newData.heartbeat);
        realtimeChart.data.datasets[1].data.push(newData.pulse);
        realtimeChart.update();

        if (historyChart.data.labels.length > 50) {
            historyChart.data.labels.shift();
            historyChart.data.datasets[0].data.shift();
            historyChart.data.datasets[1].data.shift();
        }

        historyChart.data.labels.push(timestamp);
        historyChart.data.datasets[0].data.push(newData.heartbeat);
        historyChart.data.datasets[1].data.push(newData.pulse);
        historyChart.update();
    }

    setInterval(updateCharts, 5000); // 每5秒更新一次图表
});







