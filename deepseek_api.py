from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint para procesar datos
@app.route('/procesar', methods=['GET','POST'])
def procesar():
    if request.method == 'GET':
        return jsonify({"mensaje": "Este endpoint solo acepta POST"}), 405
    else:
        # Recibe los datos enviados desde GeneXus
        data = request.json
        # Aquí puedes agregar la lógica de procesamiento con DeepSeek
        # Por ahora, simplemente devolvemos los datos recibidos como respuesta
        return jsonify({
            "status": "success",
            "mensaje": "Datos recibidos correctamente",
            "datos_recibidos": data
        })

    # Devuelve la respuesta en formato JSON
    return jsonify(respuesta)

# Inicia el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
