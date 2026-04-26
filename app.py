from flask import Flask, render_template_string
import datetime
import socket

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CI/CD Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            text-align: center;
            padding: 50px;
        }
        .card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 30px;
            margin: auto;
            width: 400px;
            box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
        }
        h1 {
            margin-bottom: 10px;
        }
        .status {
            font-size: 22px;
            color: #00ffcc;
        }
        .info {
            margin-top: 15px;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 CI/CD Pipeline</h1>
        <div class="status">Build Successful ✅</div>

        <div class="info">
            <p><b>Server:</b> {{hostname}}</p>
            <p><b>Time:</b> {{time}}</p>
            <p><b>Status:</b> Running</p>
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
        time=datetime.datetime.now()
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
