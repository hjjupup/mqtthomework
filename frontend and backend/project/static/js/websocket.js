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


