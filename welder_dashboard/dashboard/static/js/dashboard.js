// dashboard.js

alert("âœ… dashboard.js loaded!");

console.log("âœ… dashboard.js loaded to console!");





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

    const data = await fetchJSON("/api/welder/1/"); // TODO: dynamic id

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

async function updateActivityLabel(welderId = 1) {

    try {

    const data = await fetchJSON(`/api/predict-activity/?welder_id=${welderId}`);

    if (!data) return;

    document.getElementById("activity-label").textContent =

      `${data.predicted_class} (${(data.confidence * 100).toFixed(1)}%)`;

    } catch (err) {

    console.error("Activity fetch error:", err);

    }

}



const activityColors = {

    "Welding": "#ef476f",   // merah

    "Grinding": "#ffd166",  // kuning

    "Others": "#06d6a0",     // hijau

    "Preparation": "#118ab2",     // abu

    "Slag Cleaning": "#073b4c"     // biru

};



// ==================== PIE CHART ====================

let pieChart;

async function updatePieChart() {

    const data = await fetchJSON("/api/activity-stats/");

    if (!data) return;



    const labels = Object.keys(data);

    const values = Object.values(data);



    // ambil warna sesuai label

    const colors = labels.map(label => activityColors[label] || "#9ca3af");



    const ctx = document.getElementById("activity-pie").getContext("2d");

    if (!pieChart) {

        pieChart = new Chart(ctx, {

            type: "pie",

            data: {

                labels: labels,

                datasets: [{

                    data: values,

                    backgroundColor: colors

                }]

            }

        });

    } else {

        pieChart.data.labels = labels;

        pieChart.data.datasets[0].data = values;

        pieChart.data.datasets[0].backgroundColor = colors;

        pieChart.update();

    }

}



// ==================== TIMELINE ====================

let timelineData = [];  // simpan history prediksi

async function updateTimeline() {

    const data = await fetchJSON("/api/predict-activity/?welder_id=1");

    if (!data) return;



    const cls = data.predicted_class; // dari API

    timelineData.push(cls);



    // hitung distribusi

    const counts = {};

    timelineData.forEach(c => {

        counts[c] = (counts[c] || 0) + 1;

    });



    const total = timelineData.length;

    const timelineEl = document.getElementById("activity-timeline");

    timelineEl.innerHTML = "";



    // render segmen per kelas

    Object.entries(counts).forEach(([cls, count]) => {

        const span = document.createElement("span");

        span.style.width = `${(count / total) * 100}%`;  // proporsi % dari container

        span.style.backgroundColor = activityColors[cls] || "#9ca3af"; // fallback abu

        span.title = `${cls}: ${count}`;

        timelineEl.appendChild(span);

    });

}



// update tiap 3 detik (atau sesuai interval prediksi)

setInterval(updateTimeline, 3000);



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



    // Update teks terbaru

    document.getElementById("accel-x").innerText = data.ax.toFixed(2);

    document.getElementById("accel-y").innerText = data.ay.toFixed(2);

    document.getElementById("accel-z").innerText = data.az.toFixed(2);



    // Gyroscope

    gyroChart.data.labels.push(timestamp);

    gyroChart.data.datasets[0].data.push(data.gx);

    gyroChart.data.datasets[1].data.push(data.gy);

    gyroChart.data.datasets[2].data.push(data.gz);



    document.getElementById("gyro-x").innerText = data.gx.toFixed(2);

    document.getElementById("gyro-y").innerText = data.gy.toFixed(2);

    document.getElementById("gyro-z").innerText = data.gz.toFixed(2);



    // Magnetometer

    magChart.data.labels.push(timestamp);

    magChart.data.datasets[0].data.push(data.mx);

    magChart.data.datasets[1].data.push(data.my);

    magChart.data.datasets[2].data.push(data.mz);



    document.getElementById("mag-x").innerText = data.mx.toFixed(2);

    document.getElementById("mag-y").innerText = data.my.toFixed(2);

    document.getElementById("mag-z").innerText = data.mz.toFixed(2);



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
