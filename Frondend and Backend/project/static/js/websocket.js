const realtimeChart = new Chart(realtimeCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Realtime Data', data: [] }] },
});

const ws = new WebSocket('ws://localhost:5001/realtime');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Realtime data received:", data);

    const timestamp = data.timestamp;
    const payload = JSON.parse(data.payload);
    const heartbeat = payload.heartbeat;

    realtimeChart.data.labels.push(timestamp);
    realtimeChart.data.datasets[0].data.push(heartbeat);
    realtimeChart.update();
};


chart.js
const ws = new WebSocket('ws://localhost:5001/realtime');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Realtime data received:", data);

    const labels = [data.timestamp];
    const values = [JSON.parse(data.payload).heartbeat];

    realtimeChart.data.labels.push(labels);
    realtimeChart.data.datasets[0].data.push(values);
    realtimeChart.update();
};

