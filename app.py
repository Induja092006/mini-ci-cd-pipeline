from flask import Flask, render_template_string
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"

# Default values
default_data = {
    "gold": [],
    "silver": [],
    "platinum": []
}

# Load or create history file
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump(default_data, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# 🌐 Fetch real price (mock fallback)
def fetch_prices():
    try:
        # Example free API (may require key)
        url = "https://api.metals.live/v1/spot"
        res = requests.get(url, timeout=5).json()

        gold = res[0]['gold'] * 85   # convert approx to INR
        silver = res[1]['silver'] * 85
        platinum = res[2]['platinum'] * 85

        return int(gold), int(silver), int(platinum)

    except:
        # fallback values
        return 6200, 75, 2500

@app.route('/')
def home():
    data = load_data()

    gold, silver, platinum = fetch_prices()

    # Append new values
    data["gold"].append(gold)
    data["silver"].append(silver)
    data["platinum"].append(platinum)

    # Keep last 10 values
    for k in data:
        data[k] = data[k][-10:]

    save_data(data)

    def trend(arr):
        if len(arr) < 2:
            return "→"
        return "🔼" if arr[-1] > arr[-2] else "🔽"

    HTML = """
    <html>
    <head>
        <title>Metal Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg,#1f4037,#99f2c8);
                text-align: center;
                color: white;
            }

            .container {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 30px;
            }

            .card {
                background: rgba(0,0,0,0.3);
                padding: 20px;
                border-radius: 15px;
                width: 200px;
            }

            canvas {
                margin-top: 40px;
                background: white;
                border-radius: 10px;
            }
        </style>
    </head>

    <body>

    <h1>💰 Live Metal Dashboard</h1>

    <div class="container">
        <div class="card">
            <h2>Gold {{g_trend}}</h2>
            <p>₹ {{gold}}</p>
        </div>

        <div class="card">
            <h2>Silver {{s_trend}}</h2>
            <p>₹ {{silver}}</p>
        </div>

        <div class="card">
            <h2>Platinum {{p_trend}}</h2>
            <p>₹ {{platinum}}</p>
        </div>
    </div>

    <canvas id="chart" width="600" height="300"></canvas>

    <script>
        const ctx = document.getElementById('chart');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: {{labels}},
                datasets: [
                    {
                        label: 'Gold',
                        data: {{gold_data}},
                        borderColor: 'gold'
                    },
                    {
                        label: 'Silver',
                        data: {{silver_data}},
                        borderColor: 'gray'
                    },
                    {
                        label: 'Platinum',
                        data: {{platinum_data}},
                        borderColor: 'cyan'
                    }
                ]
            }
        });
    </script>

    </body>
    </html>
    """

    labels = list(range(len(data["gold"])))

    return render_template_string(
        HTML,
        gold=gold,
        silver=silver,
        platinum=platinum,
        gold_data=data["gold"],
        silver_data=data["silver"],
        platinum_data=data["platinum"],
        labels=labels,
        g_trend=trend(data["gold"]),
        s_trend=trend(data["silver"]),
        p_trend=trend(data["platinum"])
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
