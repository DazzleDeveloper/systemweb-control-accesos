from flask import Blueprint, render_template, request, redirect, url_for, flash
import cv2
import face_recognition
import os
import numpy as np
from database.db import conectar_bd
from datetime import datetime

registro = Blueprint('registro', __name__)


@registro.route('/registro', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        cargo = request.form['cargo']

        # Crear carpeta si no existe
        carpeta_rostros = 'app/static/rostros'
        os.makedirs(carpeta_rostros, exist_ok=True)

        # Inicializar cámara
        cam = cv2.VideoCapture(0)
        imagenes = []
        count = 0

        while count < 4:
            ret, frame = cam.read()
            if not ret:
                break
            cv2.imshow("Captura de rostro - Presiona 'c' para capturar", frame)
            key = cv2.waitKey(1)
            if key == ord('c'):
                ruta_imagen = f"{carpeta_rostros}/{nombre}_{count}.jpg"
                cv2.imwrite(ruta_imagen, frame)
                imagenes.append(ruta_imagen)
                count += 1

        cam.release()
        cv2.destroyAllWindows()

        # Codificar rostros y almacenar vector
        # Codificar rostros y almacenar vector
        imagen = face_recognition.load_image_file(imagenes[0])
        codificaciones = face_recognition.face_encodings(imagen)

        if not codificaciones:
            flash("❌ No se detectó ningún rostro en la imagen. Asegúrate de estar frente a la cámara.", "danger")
            return redirect(url_for('registro.registrar_usuario'))

        codificacion = codificaciones[0]
        vector = np.array(codificacion).tobytes()
        ruta_foto = imagenes[0]

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("""
                           INSERT INTO usuarios (nombre, cargo, email, ruta_foto, vector_rostro, fecha_registro)
                           VALUES (%s, %s, %s, %s, %s, %s)
                           """, (nombre, cargo, email, ruta_foto, vector, datetime.now()))
            conexion.commit()
            conexion.close()
            flash("Usuario registrado con éxito", "success")
        except Exception as e:
            flash(f"Error al registrar: {e}", "danger")

        return redirect(url_for('registro.registrar_usuario'))

    return render_template('registro.html')
