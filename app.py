from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# سجل العمليات لتخزين الحسابات السابقة
calculation_history = []

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
    data = request.get_json() or {}
    v_c = float(data.get('v_c', 0.5))
    traveler_age = float(data.get('age', 35))
    ship_mass = float(data.get('mass', 1000))
    
    # مدة الرحلة الافتراضية التي يقضيها المسافر على متن السفينة (مثلاً 10 سنوات سفينة أو مرتبطة بالعمر)
    # هنا نجعلها مدة رحلة ديناميكية أو ثابتة منطقية للمحاكاة (مثلا 10 سنوات زمن خاص للمسافر)
    proper_time = 10.0 
    
    # حساب معامل لورنتز (Gamma)
    if v_c >= 1.0:
        v_c = 0.99
    gamma = 1.0 / math.sqrt(1.0 - (v_c ** 2))
    
    # حساب الزمن على الأرض بالنسبة للمسافر
    earth_time = proper_time * gamma
    future_jump = earth_time - proper_time
    
    # طول السفينة (انكماش الطول)
    original_length = 100.0  # متر
    ship_length = original_length / gamma
    
    # طاقة الحركة (مقارنة بقنابل هيروشيما)
    c = 3e8
    kinetic_energy = (gamma - 1.0) * ship_mass * 1000 * (c ** 2)
    hiroshima_bombs = kinetic_energy / 6.3e13
    
    # المادة المضادة اللازمة للدفعة
    antimatter_tons = (kinetic_energy / (2 * (c ** 2))) / 1000
    
    # مفارقة التوأم: عمر المسافر يزيد بمدة الرحلة، وعمر الأرضي يزيد بزمن الأرض
    trav_final_age = traveler_age + proper_time
    earth_final_age = traveler_age + earth_time
    
    result_item = {
        'v_c': round(v_c, 2),
        'gamma': round(gamma, 3),
        'earth_time': round(earth_time, 2),
        'future_jump': round(future_jump, 2),
        'ship_length': round(ship_length, 2),
        'hiroshima_bombs': f"{hiroshima_bombs:,.1f}",
        'antimatter_tons': round(antimatter_tons, 2),
        'traveler_age': round(trav_final_age, 1),
        'earth_age': round(earth_final_age, 1),
        'status': 'نجاح القفزة ⚡'
    }
    
    # إضافة للسجل الاحترافي
    calculation_history.insert(0, result_item)
    if len(calculation_history) > 5:
        calculation_history.pop()
        
    result_item['history'] = calculation_history
    return jsonify(result_item)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
