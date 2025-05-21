from flask import Blueprint, render_template
from database.db import conectar_bd
import pandas as pd

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def vista_dashboard():
    conexion = conectar_bd()
    query = """
        SELECT l.id_log, u.nombre, l.estado, l.emocion, l.fecha_hora, l.ip, l.dispositivo
        FROM logs_login l
        LEFT JOIN usuarios u ON l.id_usuario = u.id_usuario
        ORDER BY l.fecha_hora DESC
    """
    df = pd.read_sql(query, conexion)
    conexion.close()

    # Datos para gráficos
    resumen_estado = df['estado'].value_counts().to_dict()
    resumen_emocion = df['emocion'].value_counts().to_dict()
    top_usuarios = df['nombre'].value_counts().head(5).to_dict()

    return render_template('dashboard.html',
                           registros=df.to_dict(orient='records'),
                           resumen_estado=resumen_estado,
                           resumen_emocion=resumen_emocion,
                           top_usuarios=top_usuarios)
