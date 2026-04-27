from flask import Flask, render_template_string, request
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ================= DB SETUP =================
conn = sqlite3.connect("prices.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gold REAL,
    silver REAL,
    platinum REAL,
    time TEXT
)
""")
conn.commit()

# ================= API =================
def fetch_prices():
    try:
        url = "https://api.metals.live/v1/spot"
        data = requests.get(url, timeout=5).json()

        gold = data[0]['gold'] * 85
        silver = data[1]['silver'] * 85
        platinum = data[2]['platinum'] * 85

        return int(gold), int(silver), int(platinum)
    except:
        return 6250, 75, 2500

# ================= ROUTE =================
@app.route('/')
def home():
    currency = request.args.get("currency", "INR")

    gold, silver, platinum = fetch_prices()

    # Currency conversion (simple)
    rates = {"INR":1, "USD":0.012, "EUR":0.011}
    rate = rates.get(currency, 1)

    gold *= rate
    silver *= rate
    platinum *= rate

    # Save to DB
    cursor.execute("INSERT INTO prices (gold, silver, platinum, time) VALUES (?,?,?,?)",
                   (gold, silver, platinum, datetime.now().strftime("%H:%M:%S")))
    conn.commit()

    # Get history
    cursor.execute("SELECT gold, silver, platinum FROM prices ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()[::-1]

    gold_data = [r[0] for r in rows]
    silver_data = [r[1] for r in rows]
    platinum_data = [r[2] for r in rows]

    # Trend arrow
    def trend(data):
        if len(data) < 2:
            return "→"
        return "🔼" if data[-1] > data[-2] else "🔽"

    # Alert
    alert = ""
    if len(gold_data) >= 2 and gold_data[-1] > gold_data[-2]:
        alert = "🚨 Gold price increased!"

    HTML = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pro Metal Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {
                font-family: Arial;
                margin: 0;
                background: linear-gradient(135deg,#141e30,#243b55);
                color: white;
                text-align: center;
            }

            .container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 15px;
                margin-top: 20px;
            }

            .card {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 15px;
                width: 250px;
            }

            select {
                padding: 8px;
                border-radius: 8px;
                margin-top: 10px;
            }

            canvas {
                margin-top: 30px;
                background: white;
                border-radius: 10px;
                width: 90% !important;
                max-width: 600px;
            }

            .alert {
                color: yellow;
                margin-top: 10px;
            }
        </style>
    </head>

    <body>

    <h2>💰 Smart Metal Dashboard</h2>

    <form method="GET">
        <select name="currency" onchange="this.form.submit()">
            <option value="INR" {% if currency=='INR' %}selected{% endif %}>INR</option>
            <option value="USD" {% if currency=='USD' %}selected{% endif %}>USD</option>
            <option value="EUR" {% if currency=='EUR' %}selected{% endif %}>EUR</option>
        </select>
    </form>

    <div class="container">
        <div class="card">
            <h3>Gold {{g_trend}}</h3>
            <p>{{gold}}</p>
        </div>

        <div class="card">
            <h3>Silver {{s_trend}}</h3>
            <p>{{silver}}</p>
        </div>

        <div class="card">
            <h3>Platinum {{p_trend}}</h3>
            <p>{{platinum}}</p>
        </div>
    </div>

    <div class="alert">{{alert}}</div>

    <canvas id="chart"></canvas>

    <script>
        setTimeout(() => location.reload(), 10000);

        new Chart(document.getElementById('chart'), {
            type: 'line',
            data: {
                labels: {{labels}},
                datasets: [
                    {label:'Gold', data: {{gold_data}}, borderColor:'gold'},
                    {label:'Silver', data: {{silver_data}}, borderColor:'gray'},
                    {label:'Platinum', data: {{platinum_data}}, borderColor:'cyan'}
                ]
            }
        });
    </script>

    </body>
    </html>
    """

    labels = list(range(len(gold_data)))

    return render_template_string(
        HTML,
        gold=round(gold,2),
        silver=round(silver,2),
        platinum=round(platinum,2),
        gold_data=gold_data,
        silver_data=silver_data,
        platinum_data=platinum_data,
        labels=labels,
        g_trend=trend(gold_data),
        s_trend=trend(silver_data),
        p_trend=trend(platinum_data),
        alert=alert,
        currency=currency
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
