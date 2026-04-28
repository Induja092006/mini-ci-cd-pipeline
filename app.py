from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle

app = Flask(__name__)

# Load trained model
model = pickle.load(open("trained_model.pkl", "rb"))

@app.route('/')
def home():
    return "🚀 AI Secure Medical Dashboard Running!"

@app.route('/health')
def health():
    return jsonify({"status": "OK"})

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    df = pd.read_csv(file)

    # Predict anomalies
    predictions = model.predict(df)

    result = []
    for i, p in enumerate(predictions):
        result.append({
            "record": i,
            "status": "⚠️ Suspicious" if p == 1 else "✅ Safe"
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
