import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint para la raíz
@app.route('/')
def index():
    return jsonify({"mensaje": "Bienvenido al servicio DeepSeek API"}), 200

# Endpoint para procesar datos
@app.route('/procesar', methods=['GET', 'POST'])
def procesar():
    if request.method == 'GET':
        return jsonify({"mensaje": "Este endpoint solo acepta POST"}), 405
    else:
        data = request.json
        return jsonify({
            "status": "success",
            "mensaje": "Datos recibidos correctamente",
            "datos_recibidos": data
        })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render asigna el puerto dinámicamente
    app.run(debug=True, host="0.0.0.0", port=port)
