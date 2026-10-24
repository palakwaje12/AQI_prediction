let aqiChart = null;

// ================= NAVIGATION =================
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function () {
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));

        this.classList.add('active');
        document.getElementById(this.dataset.page).classList.add('active');
    });
});

// ================= ANALYSIS =================
document.getElementById('analyzeBtn').addEventListener('click', async function () {
    const resultDiv = document.getElementById('result');
    const btn = this;

    const data = {
        Year: Number(year.value),
        CO: Number(co.value),
        NO2: Number(no2.value),
        O3: Number(o3.value),
        "PM2.5": Number(pm25.value),
        PM10: Number(pm10.value)
    };

    btn.disabled = true;
    btn.innerHTML = "Processing...";

    try {
        const res = await fetch("http://127.0.0.1:5001/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        resultDiv.innerHTML = `
            <div class="result-card">
                <h3>Analysis Results</h3>
                <p><b>Current AQI:</b> ${result.current_aqi}</p>
                <p><b>Future AQI (Estimated):</b> ${result.future_aqi}</p>
                <p><b>Next AQI (Forecasted):</b> ${result.next_aqi}</p>
                <p><b>Status:</b> ${result.category}</p>
            </div>
        `;

        drawAQIGraph(
            result.current_aqi,
            result.future_aqi,
            result.next_aqi
        );

    } catch {
        resultDiv.innerHTML = "Backend not reachable";
    }

    btn.disabled = false;
    btn.innerHTML = "Analyze Air Quality";
});

// ================= GRAPH =================
function drawAQIGraph(currentAQI, futureAQI, nextAQI) {
    const ctx = document.getElementById('aqiChart').getContext('2d');

    if (aqiChart) aqiChart.destroy();

    aqiChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                'Current AQI',
                'Future AQI (Estimated)',
                'Next AQI (Forecasted)'
            ],
            datasets: [{
                label: 'AQI Value',
                data: [currentAQI, futureAQI, nextAQI]
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'AQI Estimation & Next Forecast'
                }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}
