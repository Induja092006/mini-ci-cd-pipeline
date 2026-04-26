from flask import Flask, render_template_string, request

app = Flask(__name__)

gold_price = 6000  # initial price
history = [gold_price]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Gold Price Tracker</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(135deg, #1e3c72, #f7971e);
            color: white;
            text-align: center;
            padding: 40px;
        }

        .card {
            background: rgba(0,0,0,0.3);
            padding: 30px;
            border-radius: 15px;
            width: 400px;
            margin: auto;
        }

        h1 {
            margin-bottom: 10px;
        }

        .price {
            font-size: 40px;
            margin: 20px 0;
        }

        .up { color: #00ff99; }
        .down { color: #ff4d4d; }

        input {
            padding: 10px;
            border-radius: 8px;
            border: none;
            width: 80%;
            margin-top: 10px;
        }

        button {
            margin-top: 10px;
            padding: 10px;
            width: 85%;
            border: none;
            border-radius: 10px;
            background: gold;
            cursor: pointer;
        }

        .history {
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>

<div class="card">
    <h1>💰 Gold Price Tracker</h1>

    <div class="price {{trend}}">
        ₹ {{price}}
    </div>

    <form method="POST">
        <input type="number" name="new_price" placeholder="Enter new gold price" required>
        <button>Update Price</button>
    </form>

    <div class="history">
        <b>Recent Prices:</b><br>
        {% for p in history %}
            ₹ {{p}} 
        {% endfor %}
    </div>
</div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    global gold_price, history

    trend = ""

    if request.method == 'POST':
        new_price = int(request.form['new_price'])

        if new_price > gold_price:
            trend = "up"
        elif new_price < gold_price:
            trend = "down"

        gold_price = new_price
        history.append(new_price)

        if len(history) > 5:
            history.pop(0)

    return render_template_string(
        HTML,
        price=gold_price,
        history=history,
        trend=trend
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
