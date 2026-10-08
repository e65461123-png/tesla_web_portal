from flask import Flask, render_template_string, request
import math

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>محاكي النسبية والقفزات الزمنية - تسلا</title>
    <style>
        body {
            background-color: #020205;
            color: #00ffcc;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            margin: 0;
            padding: 15px;
        }
        h1 {
            font-size: 1.1rem;
            text-shadow: 0 0 10px #00ffcc;
            text-align: center;
            margin-bottom: 20px;
        }
        .panel {
            width: 100%;
            max-width: 350px;
            border: 1px solid #00ffcc;
            padding: 15px;
            background: rgba(0, 255, 204, 0.02);
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.1);
            margin-bottom: 15px;
            box-sizing: border-box;
        }
        label {
            font-size: 0.8rem;
            display: block;
            margin-bottom: 5px;
        }
        input {
            width: 100%;
            background: #030307;
            border: 1px solid #00ffcc;
            color: #00ffcc;
            padding: 8px;
            font-family: monospace;
            margin-bottom: 12px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            background: rgba(0, 255, 204, 0.15);
            border: 1px solid #00ffcc;
            color: #00ffcc;
            padding: 10px;
            font-family: monospace;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }
        button:hover {
            background: #00ffcc;
            color: #020205;
        }
        .result-box {
            font-size: 0.85rem;
            line-height: 1.6;
            border-top: 1px dashed #00ffcc;
            padding-top: 10px;
            margin-top: 10px;
        }
    </style>
</head>
<body>

    <h1>[ وحدة حساب تمدد الزمن والقفزات المستقبلية ]</h1>

    <div class="panel">
        <form method="POST" action="/">
            <label>سرعة المركبة كنسبة من سرعة الضوء (v/c):</label>
            <input type="number" name="velocity" step="0.01" min="0" max="0.99" value="{{ v }}">

            <label>مدة السفر بالزمن الذاتي (بالسنوات):</label>
            <input type="number" name="proper_time" step="1" value="{{ t0 }}">

            <button type="submit">[ تنفيذ الحساب النسبي ]</button>
        </form>

        <div class="result-box" id="output">
            {% if result %}
                > معامل لورنتز (Gamma): <strong>{{ result.gamma }}</strong><br>
                > زمن الأرض المنقضي: <strong>{{ result.earth_time }} سنة</strong><br>
                > القفزة للمستقبل: <strong>+{{ result.time_jump }} سنة</strong><br>
                > حالة الحقل: <span style="color:#ff0055">{{ result.status }}</span>
            {% else %}
                > الحالة: بانتظار الإحداثيات...<br>
            {% endif %}
        </div>
    </div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    v = 0.90
    t0 = 5
    result = None
    
    if request.method == 'POST':
        try:
            v = float(request.form.get('velocity', 0.9))
            t0 = float(request.form.get('proper_time', 5))
            
            if v >= 1.0 or v < 0:
                result = {'error': 'السرعة يجب أن تكون أقل من 1.0'}
            else:
                gamma = 1.0 / math.sqrt(1.0 - (v ** 2))
                earth_time = t0 * gamma
                time_jump = earth_time - t0
                
                result = {
                    'gamma': round(gamma, 3),
                    'earth_time': round(earth_time, 2),
                    'time_jump': round(time_jump, 2),
                    'status': 'RESONANCE_STABLE_369'
                }
        except Exception as e:
            result = {'error': str(e)}
            
    return render_template_string(HTML_TEMPLATE, v=v, t0=t0, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
