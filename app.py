from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deep Blue Calculator</title>
    <style>
        * { box-sizing: border-box; transition: all 0.2s ease; }
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #001220;
            font-family: 'Segoe UI', Roboto, sans-serif;
        }
        .calculator {
            background-color: #002b4e;
            width: 100%;
            max-width: 380px;
            padding: 30px;
            border-radius: 40px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
            border: 1px solid #004a87;
        }
        h2 { color: #80caff; text-align: center; margin-top: 0; }
        #display {
            width: 100%;
            height: 80px;
            background: #001a30;
            border: 2px solid #004a87;
            border-radius: 20px;
            margin-bottom: 25px;
            color: #ffffff;
            font-size: 2.5rem;
            text-align: right;
            padding: 20px;
        }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
        button {
            height: 70px;
            border-radius: 20px;
            border: none;
            cursor: pointer;
            font-size: 1.4rem;
            background-color: #004a87;
            color: #ffffff;
        }
        .op { background-color: #007bff; }
        .clear { grid-column: span 2; background-color: #001a30; }
        .equal { grid-column: span 2; background-color: #00d2ff; color: #002b4e; }
    </style>
</head>
<body>
    <div class="calculator">
        <h2>BLUE UI</h2>
        <input type="text" id="display" disabled value="0">
        <div class="grid">
            <button class="clear" onclick="clearD()">CLEAR</button>
            <button class="op" onclick="add('/')">÷</button>
            <button class="op" onclick="add('*')">×</button>

            <button onclick="add('7')">7</button>
            <button onclick="add('8')">8</button>
            <button onclick="add('9')">9</button>
            <button class="op" onclick="add('-')">-</button>

            <button onclick="add('4')">4</button>
            <button onclick="add('5')">5</button>
            <button onclick="add('6')">6</button>
            <button class="op" onclick="add('+')">+</button>

            <button onclick="add('1')">1</button>
            <button onclick="add('2')">2</button>
            <button onclick="add('3')">3</button>
            <button onclick="add('.')">.</button>

            <button onclick="add('0')">0</button>
            <button class="equal" onclick="calc()">=</button>
        </div>
    </div>

    <script>
        let d = document.getElementById('display');

        function add(v) {
            if (d.value === '0' && v !== '.') {
                d.value = v;
            } else {
                d.value += v;
            }
        }

        function clearD() {
            d.value = '0';
        }

        function calc() {
            try {
                d.value = eval(d.value) || '0';
            } catch {
                d.value = 'Error';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/health')
def health():
    return {"status": "OK"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
