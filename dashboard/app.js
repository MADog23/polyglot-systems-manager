const METRICS_URL = "http://localhost:9001/metrics";

async function fetchMetrics() {
  try {
    const res = await fetch(METRICS_URL);
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    const data = await res.json();

    updateCards(data);
    updateRaw(data);
  } catch (err) {
    console.error("Failed to fetch metrics:", err);
    document.getElementById("raw-metrics").textContent =
      "Error fetching metrics: " + err.message;
  }
}

function updateCards(data) {
  const cpu = document.getElementById("cpu-usage");
  const mem = document.getElementById("memory-usage");
  const uptime = document.getElementById("uptime");
  const disk = document.getElementById("disk-usage");

  if (typeof data.cpu_percent === "number") {
    cpu.textContent = data.cpu_percent.toFixed(1) + " %";
  }

  if (typeof data.memory_percent === "number") {
    mem.textContent = data.memory_percent.toFixed(1) + " %";
  }

  if (typeof data.disk_percent === "number") {
    disk.textContent = data.disk_percent.toFixed(1) + " %";
  }

  if (typeof data.uptime_seconds === "number") {
    uptime.textContent = formatUptime(data.uptime_seconds);
  }
}

function updateRaw(data) {
  const pre = document.getElementById("raw-metrics");
  if (!pre) return;
  pre.textContent = JSON.stringify(data, null, 2);
}

function formatUptime(seconds) {
  const s = Math.floor(seconds % 60);
  const m = Math.floor((seconds / 60) % 60);
  const h = Math.floor((seconds / 3600) % 24);
  const d = Math.floor(seconds / 86400);

  const parts = [];
  if (d) parts.push(d + "d");
  if (h || d) parts.push(h + "h");
  if (m || h || d) parts.push(m + "m");
  parts.push(s + "s");
  return parts.join(" ");
}

// initial fetch + poll every 1s
fetchMetrics();
setInterval(fetchMetrics, 1000);
