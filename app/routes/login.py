from flask import Blueprint, render_template, request, redirect, url_for, flash
import cv2
import face_recognition
import numpy as np
from database.db import conectar_bd
from datetime import datetime

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def login_usuario():
    mensaje = ""

    if request.method == 'POST':
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        cam.release()

        if not ret:
            flash("No se pudo acceder a la cámara", "danger")
            return redirect(url_for('login.login_usuario'))

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        codificaciones = face_recognition.face_encodings(rgb_frame)

        if not codificaciones:
            flash("❌ No se detectó ningún rostro en la imagen.", "danger")
            return redirect(url_for('login.login_usuario'))

        cod_actual = codificaciones[0]

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("SELECT id_usuario, nombre, vector_rostro FROM usuarios")
            usuarios = cursor.fetchall()

            reconocido = False
            for usuario in usuarios:
                id_usuario, nombre, vector_bytes = usuario
                vector_guardado = np.frombuffer(vector_bytes, dtype=np.float64)

                resultado = face_recognition.compare_faces([vector_guardado], cod_actual, tolerance=0.5)
                if resultado[0]:
                    reconocido = True
                    ip = request.remote_addr or "127.0.0.1"
                    cursor.execute("""
                        INSERT INTO logs_login (id_usuario, ip, estado, emocion, dispositivo)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (id_usuario, ip, 'reconocido', 'pendiente', 'PC-local'))
                    conexion.commit()
                    flash(f"✅ Usuario reconocido: {nombre}", "success")
                    break

            if not reconocido:
                cursor.execute("""
                    INSERT INTO logs_login (id_usuario, ip, estado, emocion, dispositivo)
                    VALUES (%s, %s, %s, %s, %s)
                """, (None, request.remote_addr, 'fallido', 'desconocido', 'PC-local'))
                conexion.commit()
                flash("❌ Usuario no reconocido", "danger")

            conexion.close()
        except Exception as e:
            flash(f"Error en la autenticación: {e}", "danger")

        return redirect(url_for('login.login_usuario'))

    return render_template('login.html', mensaje=mensaje)
