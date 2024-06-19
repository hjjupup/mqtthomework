const realtimeCtx = document.getElementById('realtime-chart').getContext('2d');

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

const ws = new WebSocket('ws://localhost:5001/realtime');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Realtime data received:", data);

    const timestamp = data.timestamp;
    const payload = JSON.parse(data.payload);
    const heartbeat = payload.heartbeat;

    if (realtimeChart.data.labels.length > 20) {
        realtimeChart.data.labels.shift();
        realtimeChart.data.datasets[0].data.shift();
        realtimeChart.data.datasets[1].data.shift();
    }

    realtimeChart.data.labels.push(timestamp);
    realtimeChart.data.datasets[0].data.push(heartbeat);
    realtimeChart.update();
};
