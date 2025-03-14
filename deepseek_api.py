from flask import Flask, request, jsonify
import requests

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
        
        # Extraer y devolver la respuesta
        respuesta = response.json()
        return respuesta['choices'][0]['message']['content']
    
    except Exception as e:
        # Manejo de errores
        return f"Error al procesar la pregunta: {str(e)}"

# Endpoint para procesar preguntas
@app.route('/procesar', methods=['POST'])
def procesar():
    # Recibe la pregunta desde GeneXus
    data = request.json
    pregunta = data.get("pregunta", "")
    
    # Procesa la pregunta con DeepSeek
    respuesta = deepseek_procesar(pregunta)
    
    # Devuelve la respuesta en formato JSON
    return jsonify({"respuesta": respuesta})

# Inicia el servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
