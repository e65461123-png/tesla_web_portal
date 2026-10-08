from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# قائمة لتخزين السجل
history_records = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tesla_369')
def tesla_369():
    return render_template('tesla_369.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json() or request.form
        
        v_c = float(data.get('v_c', 0.5))
        traveler_age = float(data.get('age', 35))
        ship_mass = float(data.get('mass', 1000))
        
        if v_c >= 1.0: v_c = 0.99
        if v_c < 0: v_c = 0
        
        # ═══ الحسابات ═══
        gamma = 1.0 / math.sqrt(1.0 - (v_c ** 2))
        proper_time = traveler_age
        earth_time = proper_time * gamma
        future_jump = earth_time - proper_time
        ship_length = 100.0 / gamma
        
        c = 3e8
        mass_kg = ship_mass * 1000
        kinetic_energy = (gamma - 1.0) * mass_kg * (c ** 2)
        hiroshima_bombs = kinetic_energy / 6.3e13
        antimatter_tons = kinetic_energy / (2 * (c ** 2)) / 1000
        
        traveler_final = traveler_age + proper_time
        earth_final = traveler_age + earth_time
        
        result = {
            'v_c': round(v_c, 2),
            'gamma': round(gamma, 3),
            'earth_time': round(earth_time, 2),
            'future_jump': round(future_jump, 2),
            'ship_length': round(ship_length, 1),
            'hiroshima_bombs': f"{hiroshima_bombs:,.0f}",
            'antimatter_tons': round(antimatter_tons, 2),
            'traveler_age': round(traveler_final, 1),
            'earth_age': round(earth_final, 1),
            'status': 'RESONANCE_STABLE_369'
        }
        
        history_records.insert(0, result.copy())
        if len(history_records) > 5:
            history_records.pop()
        
        return jsonify({**result, 'history': history_records})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify({'status': 'success', 'history': history_records})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
