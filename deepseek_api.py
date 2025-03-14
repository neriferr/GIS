from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Configurar la clave de API de DeepSeek
DEEPSEEK_API_KEY = "sk-48b30237594944ee8e8d82c16f1bda61"  # Tu clave de API
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # URL de la API (ajusta según la documentación de DeepSeek)

# Función para interactuar con DeepSeek
def deepseek_procesar(pregunta):
    """
    Envía una pregunta a la API de DeepSeek y obtiene una respuesta.
    
    Args:
        pregunta (str): La pregunta que se enviará a la API.
        
    Returns:
        str: La respuesta generada por la API.
    """
    try:
        # Configurar los headers con la clave de API
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Configurar el cuerpo de la solicitud
        payload = {
            "model": "deepseek-chat",  # Ajusta el modelo según la documentación de DeepSeek
            "messages": [
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": pregunta}
            ]
        }
        
        # Enviar la solicitud POST a la API de DeepSeek
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
        
        # Extraer y devolver la respuesta en UTF-8 sin BOM
        respuesta = response.json()
        respuesta_texto = respuesta['choices'][0]['message']['content']

        return respuesta_texto.encode("utf-8").decode("utf-8")  # Elimina BOM si existiera

    except Exception as e:
        return f"Error al procesar la pregunta: {str(e)}"

# Endpoint para procesar preguntas
@app.route('/procesar', methods=['POST'])
def procesar():
    try:
        # Decodificar manualmente la entrada en UTF-8 sin BOM
        raw_data = request.data.decode("utf-8-sig")  # Elimina BOM si existe
        data = json.loads(raw_data)

        pregunta = data.get("pregunta", "")
        
        # Procesa la pregunta con DeepSeek
        respuesta = deepseek_procesar(pregunta)
        
        # Devolver JSON con UTF-8 sin BOM
        #return jsonify({"respuesta": respuesta}), 200, {"Content-Type": "application/json; charset=utf-8"}
        return jsonify({"respuesta": respuesta})
    except json.JSONDecodeError:
        return jsonify({"error": "Entrada JSON inválida"}), 300
    except Exception as e:
        return jsonify({"error": f"Error al procesar la pregunta: {str(e)}"}), 500

# Inicia el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
