from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    lot_area = float(request.form['lot_area'])
    fos = float(request.form['fos']) / 100
    fot = float(request.form['fot'])
    construction_cost = float(request.form['construction_cost'])
    sale_price = float(request.form['sale_price'])

    buildable_area = lot_area * fos * fot
    common_areas = buildable_area * 0.2  # 20% common areas
    usable_area = buildable_area - common_areas
    total_cost = buildable_area * construction_cost
    total_sale_price = usable_area * sale_price
    profit = total_sale_price - total_cost

    return render_template(
        'results.html',
        buildable_area=buildable_area,
        common_areas=common_areas,
        usable_area=usable_area,
        total_cost=total_cost,
        total_sale_price=total_sale_price,
        profit=profit
    )

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto asignado por Render
    app.run(host='0.0.0.0', port=port, debug=True)
