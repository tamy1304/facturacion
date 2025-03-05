import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Inicializar CORS
CORS(app)

# Simulación de base de datos
facturas = []
factura_id = 1

# Cargar facturas desde database.json
try:
    with open('database.json', 'r') as file:
        data = json.load(file)
        facturas = data['facturas']
        if facturas:
            factura_id = max(f['id'] for f in facturas) + 1  # Ajustar id al máximo existente
except FileNotFoundError:
    print("No se encontró database.json, se usarán datos vacíos.")

@app.route('/crear_factura', methods=['POST'])
def crear_factura():
    global factura_id
    datos = request.json
    print("Datos recibidos:", data)
    nueva_factura = {
        'id': factura_id,
        'cliente': datos['cliente'],
        'producto': datos['producto'],
        'precio': datos['precio'],
        'estado': 'pendiente'
    }
    facturas.append(nueva_factura)
    factura_id += 1
    print(facturas)  # Agrega un print para verificar si las facturas están almacenadas correctamente
    return jsonify({'mensaje': 'Factura creada exitosamente', 'factura': nueva_factura})

@app.route('/facturas', methods=['GET'])
def obtener_facturas():
    return jsonify(facturas)

@app.route('/pagar_factura/<int:id>', methods=['POST'])
def pagar_factura(id):
    for factura in facturas:
        if factura['id'] == id and factura['estado'] == 'pendiente':
            factura['estado'] = 'pagada'
            return jsonify({'mensaje': f'Factura {id} pagada exitosamente'})
    return jsonify({'mensaje': 'Factura no encontrada o ya pagada'}), 404

@app.route('/notificacion', methods=['GET'])
def notificacion():
    pendientes = [f for f in facturas if f['estado'] == 'pendiente']
    return jsonify({'mensaje': f'Tienes {len(pendientes)} facturas pendientes'})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

