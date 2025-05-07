from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth, firestore
from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Obtener la ruta absoluta del archivo firebase-adminsdk.json
base_dir = os.path.dirname(os.path.abspath(__file__))
firebase_cred_path = os.path.join(base_dir, "firebase-adminsdk.json")

# Inicializar Firebase Admin SDK
cred = credentials.Certificate(firebase_cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Cargar variables de entorno
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

@app.route("/protected", methods=["GET"])
def protected_route():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Token no proporcionado"}), 401

    id_token = auth_header.split(" ")[1]

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        return jsonify({"message": f"Token válido{id_token}. UID: {uid}"})
    except Exception as e:
        return jsonify({"error": f"Token inválido: {str(e)}"}), 401


@app.route('/api/preferencias', methods=['POST'])
def guardar_preferencias():
    token = request.headers.get('Authorization').split(' ')[1]

    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        data = request.json
        doc_ref = db.collection('preferencias').document(uid)
        doc_ref.set(data)
        return jsonify({"message": "Preferencias guardadas correctamente"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "No autorizado o error al guardar preferencias"}), 401


@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    token = request.headers.get('Authorization').split(' ')[1]

    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        data = request.json
        doc_ref = db.collection('usuarios').document(uid)
        doc_ref.set(data)
        return jsonify({"message": "Usuario creado exitosamente"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error al crear usuario"}), 401


@app.route('/api/usuarios', methods=['GET'])
def obtener_usuario():
    token = request.headers.get('Authorization').split(' ')[1]

    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        doc = db.collection('usuarios').document(uid).get()

        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error al obtener usuario"}), 401


@app.route('/api/usuarios', methods=['PUT'])
def actualizar_usuario():
    token = request.headers.get('Authorization').split(' ')[1]

    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        data = request.json
        db.collection('usuarios').document(uid).update(data)
        return jsonify({"message": "Usuario actualizado correctamente"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error al actualizar usuario"}), 401


@app.route('/api/usuarios', methods=['DELETE'])
def eliminar_usuario():
    token = request.headers.get('Authorization').split(' ')[1]

    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        db.collection('usuarios').document(uid).delete()
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error al eliminar usuario"}), 401


@app.route("/api/chat", methods=["POST"])
def chat():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header:
        return jsonify({"error": "Token no proporcionado"}), 401
    try:
        token = auth_header.split(" ")[1]
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]
    except Exception as e:
        return jsonify({"error": "Token inválido o no autorizado", "detail": str(e)}), 401

    data = request.json
    user_input = data.get("mensaje")
    if not user_input:
        return jsonify({"error": "No se envió ningún mensaje"}), 400

    try:
        doc_ref = db.collection('preferencias').document(uid)
        doc = doc_ref.get()
        if doc.exists:
            preferencias = doc.to_dict()
            contexto = generar_contexto_desde_preferencias(preferencias)
        else:
            contexto = "Eres un asistente amigable y útil."
    except Exception as e:
        return jsonify({"error": "Error al obtener preferencias", "detail": str(e)}), 500

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": contexto},
                {"role": "user", "content": user_input}
            ]
        )
        respuesta = response.choices[0].message.content
        return jsonify({"respuesta": respuesta}), 200
    except Exception as e:
        return jsonify({"error": "Error al generar respuesta", "detail": str(e)}), 500


def generar_contexto_desde_preferencias(preferencias):
    nombre = preferencias.get("nombre", "usuario")
    tono = preferencias.get("tono", "amigable")
    intereses = preferencias.get("intereses", [])
    objetivo = preferencias.get("objetivo", "ayuda general")
    pronombres = preferencias.get("pronombre", "femenino")

    intereses_str = ", ".join(intereses) if isinstance(intereses, list) else intereses

    return (
        f"El nombre de usuario es: {nombre}. "
        f"Eres un asistente con tono {tono}. "
        f"Este usuario está interesado en {intereses_str}. "
        f"Su objetivo es {objetivo}. "
        f"Pronombres del usuario: {pronombres}. "
        "Responde de forma personalizada, empática y brinda apoyo emocional."
    )


if __name__ == "__main__":
    app.run(debug=True)
