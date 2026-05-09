// Dashboard update intervals
const METRICS_INTERVAL = 1000;   // 1 second
const SERVICES_INTERVAL = 2000;  // 2 seconds

// DOM elements
const cpuEl = document.getElementById("cpu-value");
const memoryEl = document.getElementById("memory-value");
const diskEl = document.getElementById("disk-value");
const uptimeEl = document.getElementById("uptime-value");
const servicesBody = document.getElementById("services-body");

// Format uptime seconds into human-readable text
function formatUptime(seconds) {
    if (seconds == null) return "--";
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs}h ${mins}m ${secs}s`;
}

// Fetch and update system metrics
async function updateMetrics() {
    try {
        const res = await fetch("/api/metrics");
        const data = await res.json();

        cpuEl.textContent = data.cpu_percent != null ? `${data.cpu_percent.toFixed(1)}%` : "--%";
        memoryEl.textContent = data.memory_percent != null ? `${data.memory_percent.toFixed(1)}%` : "--%";
        diskEl.textContent = data.disk_percent != null ? `${data.disk_percent.toFixed(1)}%` : "--%";
        uptimeEl.textContent = formatUptime(data.uptime_seconds);
    } catch (err) {
        console.error("Failed to fetch metrics:", err);
    }
}

// Fetch and update service table
async function updateServices() {
    try {
        const res = await fetch("/api/services");
        const services = await res.json();

        servicesBody.innerHTML = "";

        services.forEach(svc => {
            const row = document.createElement("tr");

            const name = document.createElement("td");
            name.textContent = svc.name;

            const running = document.createElement("td");
            running.textContent = svc.running ? "Yes" : "No";
            running.className = svc.running ? "ok" : "bad";

            const healthy = document.createElement("td");
            healthy.textContent = svc.healthy ? "Healthy" : "Unhealthy";
            healthy.className = svc.healthy ? "ok" : "bad";

            const restarts = document.createElement("td");
            restarts.textContent = svc.restarts;

            row.appendChild(name);
            row.appendChild(running);
            row.appendChild(healthy);
            row.appendChild(restarts);

            servicesBody.appendChild(row);
        });
    } catch (err) {
        console.error("Failed to fetch services:", err);
    }
}

// Start polling loops
setInterval(updateMetrics, METRICS_INTERVAL);
setInterval(updateServices, SERVICES_INTERVAL);

// Initial load
updateMetrics();
updateServices();
