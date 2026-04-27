from flask import Flask, render_template_string, request
import requests
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ================= DB =================
def get_db():
    conn = sqlite3.connect("prices.db")
    return conn


# Create table safely
conn = get_db()
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
conn.close()


# ================= API =================
def fetch_prices():
    try:
        url = "https://api.metals.live/v1/spot"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            raise Exception("API failed")

        data = response.json()

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

    rates = {"INR": 1, "USD": 0.012, "EUR": 0.011}
    rate = rates.get(currency, 1)

    gold *= rate
    silver *= rate
    platinum *= rate

    # DB insert
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO prices (gold, silver, platinum, time) VALUES (?,?,?,?)",
        (gold, silver, platinum, datetime.now().strftime("%H:%M:%S"))
    )

    conn.commit()

    cursor.execute("SELECT gold, silver, platinum FROM prices ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()[::-1]
    conn.close()

    gold_data = [r[0] for r in rows]
    silver_data = [r[1] for r in rows]
    platinum_data = [r[2] for r in rows]

    def trend(data):
        if len(data) < 2:
            return "→"
        return "🔼" if data[-1] > data[-2] else "🔽"

    alert = ""
    if len(gold_data) >= 2 and gold_data[-1] > gold_data[-2]:
        alert = "🚨 Gold price increased!"

    HTML = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart Metal Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body style="font-family:Arial;text-align:center;background:#222;color:white;">

        <h2>💰 Smart Metal Dashboard</h2>

        <form method="GET">
            <select name="currency" onchange="this.form.submit()">
                <option value="INR" {% if currency=='INR' %}selected{% endif %}>INR</option>
                <option value="USD" {% if currency=='USD' %}selected{% endif %}>USD</option>
                <option value="EUR" {% if currency=='EUR' %}selected{% endif %}>EUR</option>
            </select>
        </form>

        <h3>Gold {{g_trend}} : {{gold}}</h3>
        <h3>Silver {{s_trend}} : {{silver}}</h3>
        <h3>Platinum {{p_trend}} : {{platinum}}</h3>

        <p style="color:yellow">{{alert}}</p>

        <canvas id="chart"></canvas>

        <script>
            setTimeout(() => location.reload(), 10000);

            new Chart(document.getElementById('chart'), {
                type: 'line',
                data: {
                    labels: {{labels}},
                    datasets: [
                        {label:'Gold', data: {{gold_data}}},
                        {label:'Silver', data: {{silver_data}}},
                        {label:'Platinum', data: {{platinum_data}}}
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
        gold=round(gold, 2),
        silver=round(silver, 2),
        platinum=round(platinum, 2),
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
