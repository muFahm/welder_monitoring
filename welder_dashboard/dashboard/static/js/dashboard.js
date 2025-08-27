// dashboard.js
alert("✅ dashboard.js loaded!");
console.log("✅ dashboard.js loaded to console!");

import { Chart } from "chart.js";

// ==================== CLOCK ====================
function startClock() {
    const clockEl = document.getElementById("dashboard-clock");
    setInterval(() => {
        const now = new Date();
        clockEl.textContent = now.toLocaleTimeString();
    }, 1000);
}

// ==================== FETCH HELPERS ====================
async function fetchJSON(url) {
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP error! ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error("Fetch error:", err);
        return null;
    }
}

// ==================== WELDER PROFILE ====================
async function loadWelderProfile() {
    const data = await fetchJSON("/api/welder/<id>/"); // TODO: dynamic id
    if (!data) return;

    document.getElementById("welder-photo").src = data.photo_url;
    document.getElementById("welder-name").textContent = data.name;
    document.getElementById("welder-email").textContent = data.email;
    document.getElementById("welder-phone").textContent = data.phone;
    document.getElementById("welder-skills").textContent = data.skills.join(", ");
    document.getElementById("welder-experience").textContent = `${data.experience} years`;
    document.getElementById("welder-cert-id").textContent = data.certification_id;
    document.getElementById("welder-cert-body").textContent = data.certification_body;
    document.getElementById("welder-cert-expiry").textContent = data.certification_expiry;
}

// ==================== ACTIVITY LABEL ====================
async function updateActivityLabel() {
    const data = await fetchJSON("/api/predict-activity/?welder_id=1");
    if (!data) return;
    document.getElementById("activity-label").textContent = `${data.predicted_class} (${(data.confidence*100).toFixed(1)}%)`;
}

// ==================== PIE CHART ====================
let pieChart;
async function updatePieChart() {
    const data = await fetchJSON("/api/activity-stats/");
    if (!data) return;

    const ctx = document.getElementById("activity-pie").getContext("2d");
    if (!pieChart) {
        pieChart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(data),
                datasets: [{
                    data: Object.values(data),
                }]
            }
        });
    } else {
        pieChart.data.datasets[0].data = Object.values(data);
        pieChart.update();
    }
}

// ==================== TIMELINE ====================
async function updateTimeline() {
    const data = await fetchJSON("/api/sensor-data/");
    if (!data) return;

    const timelineEl = document.getElementById("activity-timeline");
    timelineEl.innerHTML = "";

    data.forEach(segment => {
        const span = document.createElement("span");
        span.className = `timeline-segment ${segment.class}`;
        span.style.width = `${segment.width}%`;
        timelineEl.appendChild(span);
    });
}

// ==================== SENSOR CHARTS ====================
let accelChart, gyroChart, magChart;
function initSensorCharts() {
    accelChart = new Chart(document.getElementById("accel-chart"), {
        type: "line",
        data: { labels: [], datasets: [
            { label: "Ax", data: [] },
            { label: "Ay", data: [] },
            { label: "Az", data: [] },
        ]}
    });

    gyroChart = new Chart(document.getElementById("gyro-chart"), {
        type: "line",
        data: { labels: [], datasets: [
            { label: "Gx", data: [] },
            { label: "Gy", data: [] },
            { label: "Gz", data: [] },
        ]}
    });

    magChart = new Chart(document.getElementById("mag-chart"), {
        type: "line",
        data: { labels: [], datasets: [
            { label: "Mx", data: [] },
            { label: "My", data: [] },
            { label: "Mz", data: [] },
        ]}
    });
}

async function updateSensorCharts() {
    const data = await fetchJSON("/api/sensor/latest/");
    if (!data) return;

    const timestamp = new Date(data.timestamp).toLocaleTimeString();

    // Accelerometer
    accelChart.data.labels.push(timestamp);
    accelChart.data.datasets[0].data.push(data.ax);
    accelChart.data.datasets[1].data.push(data.ay);
    accelChart.data.datasets[2].data.push(data.az);

    // Gyroscope
    gyroChart.data.labels.push(timestamp);
    gyroChart.data.datasets[0].data.push(data.gx);
    gyroChart.data.datasets[1].data.push(data.gy);
    gyroChart.data.datasets[2].data.push(data.gz);

    // Magnetometer
    magChart.data.labels.push(timestamp);
    magChart.data.datasets[0].data.push(data.mx);
    magChart.data.datasets[1].data.push(data.my);
    magChart.data.datasets[2].data.push(data.mz);

    // Limit to last 60 points (1 minute if per sec)
    [accelChart, gyroChart, magChart].forEach(chart => {
        if (chart.data.labels.length > 60) {
            chart.data.labels.shift();
            chart.data.datasets.forEach(ds => ds.data.shift());
        }
        chart.update();
    });
}

// ==================== INIT ====================
document.addEventListener("DOMContentLoaded", () => {
    startClock();
    loadWelderProfile();
    initSensorCharts();

    // Update prediction-driven components
    setInterval(updateActivityLabel, 2000);
    setInterval(updatePieChart, 5000);
    setInterval(updateTimeline, 5000);

    // Update sensor charts
    setInterval(updateSensorCharts, 1000);
});
