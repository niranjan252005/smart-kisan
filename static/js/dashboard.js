const API = "http://localhost:5000";

// ------------------ LOAD DASHBOARD ---------------------
async function loadDashboard() {
    loadWeather();
    loadCrops();
    loadSoil();
    loadMarketPrices();
    loadSchemes();
    loadNotifications();
}

// ------------------- WEATHER -------------------------
async function loadWeather() {
    const res = await fetch(`${API}/weather/today`);
    const data = await res.json();

    document.getElementById("location").innerText = data.location;
    document.getElementById("temp").innerText = data.temp + "°C";
    document.getElementById("condition").innerText = data.condition;
    document.getElementById("humidity").innerText = data.humidity + "%";
    document.getElementById("wind").innerText = data.wind + " km/h";
}

// ------------------- CROP RECOMMENDATIONS -------------------------
async function loadCrops() {
    const res = await fetch(`${API}/crop/recommend`);
    const crops = await res.json();

    let html = "";
    crops.forEach(c => {
        html += `
            <div class='crop-item'>
                <b>${c.name}</b>
                <p>${c.season}</p>
                <span class='match'>${c.match}% Match</span>
            </div>
        `;
    });

    document.getElementById("crop-list").innerHTML = html;
}

// ------------------- SOIL HEALTH -------------------------
async function loadSoil() {
    const res = await fetch(`${API}/soil/latest`);
    const soil = await res.json();

    document.getElementById("soil-data").innerHTML = `
        <p>Nitrogen: <b>${soil.n}</b></p>
        <p>Phosphorus: <b>${soil.p}</b></p>
        <p>Potassium: <b>${soil.k}</b></p>
    `;
}

// ------------------- MARKET PRICES -------------------------
async function loadMarketPrices() {
    const res = await fetch(`${API}/market/prices`);
    const data = await res.json();

    let html = "";
    data.forEach(item => {
        html += `
            <div class="market-item">
                <b>${item.crop}</b>
                <p>₹${item.price}/quintal</p>
                <span class="change">${item.change}%</span>
            </div>
        `;
    });

    document.getElementById("market-list").innerHTML = html;
}

// ------------------- GOV. SCHEMES -------------------------
async function loadSchemes() {
    const res = await fetch(`${API}/schemes`);
    const schemes = await res.json();

    let html = "";
    schemes.forEach(s => {
        html += `
            <div class="scheme-card">
                <h4>${s.title}</h4>
                <p>${s.desc}</p>
                <button>Learn More</button>
            </div>
        `;
    });

    document.getElementById("schemes").innerHTML = html;
}

// ------------------- NOTIFICATIONS -------------------------
async function loadNotifications() {
    const res = await fetch(`${API}/notifications`);
    const list = await res.json();

    let html = "";
    list.forEach(n => {
        html += `<p>🔔 ${n.message}</p>`;
    });

    document.getElementById("notif-list").innerHTML = html;
}


// ---------- Notification Panel ------------
function openNotifications() {
    document.getElementById("notification-panel").style.right = "0";
}
function closeNotifications() {
    document.getElementById("notification-panel").style.right = "-300px";
}

// Load everything
loadDashboard();
// 1️⃣ WEATHER
async function loadWeather() {
    const res = await fetch("http://localhost:5000/weather/today");
    const data = await res.json();

    document.getElementById("temp").innerHTML = data.temp + "°C";
    document.getElementById("humidity").innerHTML = data.humidity + "%";
    document.getElementById("wind").innerHTML = data.wind + " km/h";
}


// 2️⃣ CROP RECOMMENDATION
async function loadCrops() {
    const res = await fetch("http://localhost:5000/crop/recommend");
    const crops = await res.json();

    let html = "";
    crops.forEach(c => {
        html += `
            <p><b>${c.name}</b> — ${c.season} (${c.match}% match)</p>
        `;
    });

    document.getElementById("crop-list").innerHTML = html;
}


// 3️⃣ SOIL HEALTH
async function loadSoil() {
    const res = await fetch("http://localhost:5000/soil/latest");
    const data = await res.json();

    document.getElementById("soil-n").innerHTML = data.n;
    document.getElementById("soil-p").innerHTML = data.p;
    document.getElementById("soil-k").innerHTML = data.k;
}


// 4️⃣ MARKET PRICES
async function loadMarketPrices() {
    const res = await fetch("http://localhost:5000/market/prices");
    const items = await res.json();

    let html = "";
    items.forEach(m => {
        html += `
            <p><b>${m.crop}</b> — ₹${m.price} (Change: ${m.change}%)</p>
        `;
    });

    document.getElementById("market-list").innerHTML = html;
}


// 5️⃣ GOVT SCHEMES
async function loadSchemes() {
    const res = await fetch("http://localhost:5000/schemes");
    const items = await res.json();

    let html = "";
    items.forEach(s => {
        html += `
            <p><b>${s.title}</b>: ${s.desc}</p>
        `;
    });

    document.getElementById("scheme-list").innerHTML = html;
}


// 🔄 LOAD ALL WIDGETS ON PAGE LOAD
window.onload = () => {
    loadWeather();
    loadCrops();
    loadSoil();
    loadMarketPrices();
    loadSchemes();
};
// ----------------------
// CAMERA CAPTURE
// ----------------------

/* 📸 REAL-WORKING CAMERA CAPTURE HERE */
async function openCamera() {
  const video = document.getElementById("camera");
  const canvas = document.getElementById("snapshot");
  const preview = document.getElementById("preview");

  // Show video (camera preview)
  video.style.display = "block";

  // ask for camera permission
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.srcObject = stream;

  // After 3 seconds capture image
  setTimeout(() => {
      const context = canvas.getContext("2d");

      canvas.style.display = "block";
      preview.style.display = "block";

      // Capture frame
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Stop camera after capture
      stream.getTracks().forEach(track => track.stop());

      // Convert image to base64 and preview
      preview.src = canvas.toDataURL("image/png");

      console.log("Photo captured!");

  }, 3000);
}


// Upload to Flask
function uploadImage(dataURL) {
    fetch("/api/upload-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: dataURL })
    })
    .then(res => res.json())
    .then(data => console.log("Image saved:", data));
}



// -----------------------------------
// GRAPH SECTION (Chart.js)
// -----------------------------------

function loadGraphs() {
    fetch("/api/weather")
        .then(res => res.json())
        .then(data => {
            new Chart(document.getElementById("weatherGraph"), {
                type: "line",
                data: {
                    labels: ["Temp", "Humidity", "Wind"],
                    datasets: [{
                        label: "Weather Stats",
                        data: [data.temp, data.humidity, data.wind]
                    }]
                }
            });
        });

    fetch("/api/soil")
        .then(res => res.json())
        .then(data => {
            new Chart(document.getElementById("soilGraph"), {
                type: "bar",
                data: {
                    labels: ["N", "P", "K", "Moisture"],
                    datasets: [{
                        label: "Soil Health",
                        data: [data.N, data.P, data.K, data.moisture]
                    }]
                }
            });
        });

    fetch("/api/market")
        .then(res => res.json())
        .then(data => {
            const names = data.slice(0, 5).map(x => x.crop);
            const prices = data.slice(0, 5).map(x => x.price);

            new Chart(document.getElementById("marketGraph"), {
                type: "line",
                data: {
                    labels: names,
                    datasets: [{
                        label: "Market Price",
                        data: prices
                    }]
                }
            });
        });
}

loadGraphs();
