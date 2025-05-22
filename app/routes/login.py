from flask import Blueprint, render_template, request, jsonify
import face_recognition
import numpy as np
import base64
from datetime import datetime
from database.db import conectar_bd
from PIL import Image
from io import BytesIO
from deepface import DeepFace

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def login_usuario():
    if request.method == 'GET':
        return render_template('login.html')

    try:
        data = request.get_json()
        imagen_base64 = data['imagen']

        # Decodificar imagen
        img_data = base64.b64decode(imagen_base64.split(',')[1])
        image = face_recognition.load_image_file(BytesIO(img_data))

        # Codificar rostro actual
        codificaciones = face_recognition.face_encodings(image)
        if not codificaciones:
            return jsonify({'error': '❌ No se detectó ningún rostro en la imagen'}), 400

        cod_actual = codificaciones[0]

        # Analizar emoción
        img_pil = Image.open(BytesIO(img_data))
        img_pil.save("temp_login.jpg")  # Temporal

        try:
            resultado = DeepFace.analyze(img_path="temp_login.jpg", actions=['emotion'], enforce_detection=False)
            emocion_detectada = resultado[0]['dominant_emotion']
        except Exception as e:
            emocion_detectada = "neutral"

        # Traducir emociones
        traduccion_emociones = {
            "happy": "feliz",
            "sad": "triste",
            "neutral": "neutral",
            "angry": "enojado",
            "surprise": "sorprendido",
            "fear": "asustado",
            "disgust": "disgustado"
        }
        emocion_db = traduccion_emociones.get(emocion_detectada, "neutral")

        # Verificar contra usuarios registrados
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre, vector_rostro FROM usuarios")
        usuarios = cursor.fetchall()

        for id_usuario, nombre, vector_bytes in usuarios:
            vector_guardado = np.frombuffer(vector_bytes, dtype=np.float64)
            resultado = face_recognition.compare_faces([vector_guardado], cod_actual, tolerance=0.5)
            if resultado[0]:
                # Registrar acceso
                cursor.execute("""
                    INSERT INTO logs_login (id_usuario, ip, estado, emocion, dispositivo)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_usuario, request.remote_addr, 'reconocido', emocion_db, 'Webcam Navegador'))
                conexion.commit()
                conexion.close()
                return jsonify({'mensaje': f"✅ Bienvenido {nombre}"}), 200

        # Si no fue reconocido
        cursor.execute("""
            INSERT INTO logs_login (id_usuario, ip, estado, emocion, dispositivo)
            VALUES (%s, %s, %s, %s, %s)
        """, (None, request.remote_addr, 'fallido', emocion_db, 'Webcam Navegador'))
        conexion.commit()
        conexion.close()
        return jsonify({'error': '❌ Usuario no reconocido'}), 401

    except Exception as e:
        return jsonify({'error': f"❌ Error al procesar imagen: {str(e)}"}), 500
