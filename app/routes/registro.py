from deepface import DeepFace
from flask import Blueprint, request, jsonify, render_template
import face_recognition
import numpy as np
import base64
import os
from datetime import datetime
from database.db import conectar_bd
from PIL import Image
from io import BytesIO

dashboard = Blueprint('dashboard', __name__)
registro = Blueprint('registro', __name__)

@registro.route('/registro', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'GET':
        return render_template('registro.html')

    try:
        data = request.get_json()
        nombre = data['nombre']
        email = data['email']
        cargo = data['cargo']
        emocion = data.get('emocion', 'No detectado')  # Emoción enviada desde frontend
        imagenes_base64 = data['imagenes']  # Lista de 4 imágenes

        if not imagenes_base64 or len(imagenes_base64) < 4:
            return jsonify({'error': 'Se requieren 4 imágenes'}), 400

        carpeta = 'app/static/rostros'
        os.makedirs(carpeta, exist_ok=True)

        vector = None
        ruta_guardada = None

        for idx, base64_img in enumerate(imagenes_base64):
            img_data = base64.b64decode(base64_img.split(',')[1])
            img_path = f"{carpeta}/{nombre}_{idx}.jpg"

            with open(img_path, 'wb') as f:
                f.write(img_data)

            image = face_recognition.load_image_file(BytesIO(img_data))
            codificaciones = face_recognition.face_encodings(image)

            if codificaciones:
                vector = np.array(codificaciones[0]).tobytes()
                ruta_guardada = img_path
                break

        if vector is None:
            return jsonify({'error': '❌ No se detectó ningún rostro válido en las imágenes'}), 400

        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre, cargo, email, ruta_foto, vector_rostro, fecha_registro, emocion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, cargo, email, ruta_guardada, vector, datetime.now(), emocion))
        print(f"[OK] Usuario registrado: {nombre} - {email} - Emoción: {emocion}")
        conexion.commit()
        conexion.close()

        return jsonify({'mensaje': '✅ Usuario registrado con éxito'}), 200

    except Exception as e:
        return jsonify({'error': f'❌ Error al registrar: {str(e)}'}), 500


@dashboard.route('/dashboard')
def vista_dashboard():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT l.id_log, u.nombre, l.fecha_hora, l.estado, l.emocion, l.ip, l.dispositivo
        FROM logs_login l
        LEFT JOIN usuarios u ON l.id_usuario = u.id_usuario
        ORDER BY l.fecha_hora DESC
        LIMIT 50
    """)
    registros = cursor.fetchall()
    conexion.close()

    return render_template('dashboard.html', registros=registros)


@dashboard.route('/detectar_emocion', methods=['POST'])
def detectar_emocion():
    try:
        data = request.get_json()
        imagen_base64 = data['imagen']
        img_data = base64.b64decode(imagen_base64.split(',')[1])

        img_pil = Image.open(BytesIO(img_data))
        img_pil.save("temp_emocion.jpg")

        resultado = DeepFace.analyze(
            img_path="temp_emocion.jpg",
            actions=['emotion'],
            detector_backend='retinaface',
            enforce_detection=True
        )
        emocion_detectada = resultado[0]['dominant_emotion']

        return jsonify({"emocion": emocion_detectada}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
