from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth, firestore


app = Flask(__name__)
CORS(app)  # Permite peticiones desde el frontend

# Inicializar Firebase Admin SDK
cred = credentials.Certificate("project\\firebase-adminsdk.json")  # archivo JSON descargado de Firebase
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
        return jsonify({"message": f"Token válidoo. UID: {uid}"})
    except Exception as e:
        return jsonify({"error": f"Token inválidoo: {str(e)}"}), 401
    
@app.route('/api/preferencias', methods=['POST'])
def guardar_preferencias():
    # Verifica el token del usuario
    token = request.headers.get('Authorization').split(' ')[1]
    
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        # Obtener los datos enviados desde el frontend
        data = request.json
        
        # Guardar las preferencias en Firestore
        doc_ref = db.collection('preferencias').document(uid)
        doc_ref.set(data)
        
        return jsonify({"message": "Preferencias guardadas correctamente"}), 200
    
    except Exception as e:
        print(f"Error al verificar el token o guardar los datos: {e}")
        return jsonify({"error": "No autorizado o error al guardar preferencias"}), 401

if __name__ == "__main__":
    app.run(debug=True)
