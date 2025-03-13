import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint para la raíz
@app.route('/')
def index():
    return jsonify({"mensaje": "Bienvenido al servicio DeepSeek API 200"}), 200

# Endpoint para procesar datos
@app.route('/procesar', methods=['POST'])
def procesar():
    # Recibe los datos enviados desde GeneXus
    data = request.get_json()
    
    if data is None:
        return jsonify({"status": "error", "mensaje": "Solicitud inválida, envíe datos en formato JSON"}), 400
    
    # Aquí puedes agregar la lógica de procesamiento con DeepSeek
    return jsonify({
        "status": "success",
        "mensaje": "Datos recibidos correctamente",
        "datos_recibidos": data
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render asigna el puerto dinámicamente
    app.run(debug=True, host="0.0.0.0", port=port)
