from flask import Flask, render_template_string

app = Flask(__name__)

# 🔥 CHANGE THESE VALUES WHEN MARKET UPDATES
gold_price = 6200
silver_price = 75
platinum_price = 2500

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Metal Price Dashboard</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1f1c2c, #928dab);
            color: white;
            text-align: center;
        }

        h1 {
            margin-top: 30px;
        }

        .container {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 50px;
        }

        .card {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 20px;
            width: 200px;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 20px rgba(0,0,0,0.4);
            transition: 0.3s;
        }

        .card:hover {
            transform: scale(1.05);
        }

        .price {
            font-size: 28px;
            margin-top: 10px;
        }

        .gold { color: gold; }
        .silver { color: #c0c0c0; }
        .platinum { color: #00e6e6; }

        .footer {
            margin-top: 40px;
            font-size: 14px;
            color: #ddd;
        }
    </style>
</head>
<body>

<h1>💰 Live Metal Prices</h1>

<div class="container">

    <div class="card">
        <h2 class="gold">Gold</h2>
        <div class="price">₹ {{gold}}</div>
    </div>

    <div class="card">
        <h2 class="silver">Silver</h2>
        <div class="price">₹ {{silver}}</div>
    </div>

    <div class="card">
        <h2 class="platinum">Platinum</h2>
        <div class="price">₹ {{platinum}}</div>
    </div>

</div>

<div class="footer">
    🔄 Updated via CI/CD Pipeline
</div>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(
        HTML,
        gold=gold_price,
        silver=silver_price,
        platinum=platinum_price
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
