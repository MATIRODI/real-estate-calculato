from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Inputs del usuario
    lot_area = float(request.form['lot_area'])  # Área del lote
    fos = float(request.form['fos']) / 100  # FOS convertido a decimal
    fot = float(request.form['fot'])  # FOT ingresado por el usuario
    local_size = float(request.form['local_size'])  # Tamaño promedio por local comercial
    build_locals = 'build_locals' in request.form  # Checkbox para locales comerciales

    # Cálculos básicos
    total_buildable_area = lot_area * fot  # Área construible total
    ground_floor_area = lot_area * fos  # Área ocupada en planta baja

    # Validación de datos
    if local_size < 20:
        return "El tamaño promedio por local debe ser al menos 20 m².", 400

    # Renderizar resultados de la primera etapa
    return render_template(
        'results_stage1.html',
        total_buildable_area=total_buildable_area,
        ground_floor_area=ground_floor_area,
        lot_area=lot_area,
        fos=fos,
        fot=fot,
        local_size=local_size,
        build_locals=build_locals
    )

@@app.route('/calculate', methods=['POST'])
def calculate():
    # Inputs del usuario
    lot_area = float(request.form['lot_area'])  # Área del lote
    fot = float(request.form['fot'])  # FOT ingresado por el usuario

    # Cálculo del área construible total
    total_buildable_area = lot_area * fot

    # Pasar a la etapa 2
    return render_template(
        'results_stage1.html',
        total_buildable_area=total_buildable_area,
        lot_area=lot_area,
        fot=fot
    )

@app.route('/stage2', methods=['POST'])
def stage2():
    # Datos de la primera etapa
    total_buildable_area = float(request.form['total_buildable_area'])
    lot_area = float(request.form['lot_area'])
    fot = float(request.form['fot'])

    # Inputs de la etapa 2
    fos = float(request.form['fos']) / 100  # FOS convertido a decimal
    build_locals = 'build_locals' in request.form  # Checkbox para locales comerciales
    local_count = int(request.form['local_count']) if 'local_count' in request.form and request.form['local_count'] else 0

    # Cálculo del área de planta baja
    ground_floor_area = lot_area * fos

    # Validación de locales comerciales
    if build_locals:
        max_locals = ground_floor_area // 100  # Asumimos locales de 100 m²
        if local_count > max_locals:
            return f"No es posible construir {local_count} locales. Máximo permitido: {int(max_locals)}.", 400

    # Distribuir área restante para departamentos
    if build_locals:
        area_pb_usada = local_count * 100
        departamentos_pb = (ground_floor_area - area_pb_usada) // 50
    else:
        departamentos_pb = ground_floor_area // 50
        local_count = 0

    # Calcular resultados adicionales
    total_cost = total_buildable_area * 300  # Costo estimado por m²
    total_ingresos = departamentos_pb * 50000 + local_count * 100000
    beneficio = total_ingresos - total_cost

    return render_template(
        'results_stage2.html',
        total_buildable_area=total_buildable_area,
        ground_floor_area=ground_floor_area,
        departamentos_pb=departamentos_pb,
        local_count=local_count,
        total_cost=total_cost,
        total_ingresos=total_ingresos,
        beneficio=beneficio
    )



import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto asignado por Render
    app.run(host='0.0.0.0', port=port, debug=True)
