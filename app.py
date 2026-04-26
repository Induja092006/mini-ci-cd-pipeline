from flask import Flask, render_template_string
import datetime
import socket
import random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Live Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
            text-align: center;
        }

        .container {
            margin-top: 60px;
        }

        .card {
            background: rgba(255,255,255,0.08);
            padding: 30px;
            border-radius: 20px;
            width: 420px;
            margin: auto;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 30px rgba(0,0,0,0.5);
            transition: transform 0.3s;
        }

        .card:hover {
            transform: scale(1.05);
        }

        h1 {
            margin-bottom: 10px;
        }

        .status {
            font-size: 22px;
            color: #00ffcc;
            margin-bottom: 20px;
        }

        .info {
            font-size: 16px;
            text-align: left;
            margin-top: 20px;
        }

        .progress {
            background: #333;
            border-radius: 20px;
            overflow: hidden;
            margin-top: 20px;
        }

        .progress-bar {
            height: 20px;
            width: {{progress}}%;
            background: linear-gradient(90deg, #00ffcc, #00ccff);
            transition: width 1s;
        }

        .footer {
            margin-top: 20px;
            font-size: 14px;
            color: #aaa;
        }
    </style>
</head>
<body>

<div class="container">
    <div class="card">
        <h1>🚀 DevOps Dashboard</h1>
        <div class="status">Pipeline Running ✅</div>

        <div class="progress">
            <div class="progress-bar"></div>
        </div>

        <div class="info">
            <p><b>Server:</b> {{hostname}}</p>
            <p><b>Time:</b> {{time}}</p>
            <p><b>Build:</b> SUCCESS</p>
        </div>

        <div class="footer">
            Auto-refresh every 5 seconds 🔄
        </div>
    </div>
</div>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(
        HTML,
        hostname=socket.gethostname(),
        time=datetime.datetime.now(),
        progress=random.randint(70, 100)
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
