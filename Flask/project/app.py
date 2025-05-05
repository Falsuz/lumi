from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth, firestore

app = Flask(__name__)
CORS(app)

# Inicializar Firebase Admin SDK
cred = credentials.Certificate("project\\firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


@app.route("/protected", methods=["GET"])
def protected_route():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Token no proporcionado"}), 401

    id_token = auth_header.split(" ")[1]

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        return jsonify({"message": f"Token válido. UID: {uid}"})
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


# ========== CRUD de USUARIOS ==========

# Crear usuario
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


# Obtener información del usuario
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


# Actualizar información del usuario
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


# Eliminar usuario
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


if __name__ == "__main__":
    app.run(debug=True)
