from database.db import conectar_bd

try:
    conexion = conectar_bd()
    print("✅ Conexión exitosa a MySQL")
    conexion.close()
except Exception as e:
    print(f"❌ Error al conectar: {e}")
